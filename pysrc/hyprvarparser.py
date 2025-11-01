import os
import re
from typing import List, Any, cast
from warnings import resetwarnings
from hyprvar import HyprVar
from glog import logger

def _unpack_arithmetic(expression : str, vars : List[HyprVar]) -> str:
    arith_valid_pattern : str = r"^\{\{[^{}]+ [+\-/*] [^{}]+\}\}$"
    match = re.match(arith_valid_pattern, expression)
    if match is None:
        logger.error(f"hyprlang parser > invalid arithmetic structure ({expression})")
        return expression 

    textvars = re.findall(r"[a-zA-Z_]\w*", expression)
    if len(textvars) != 2:
        logger.error(f"hyprlang parser > invalid amount of variables at '{expression}' (this shouldnt happen)")
        return expression 

    for i in textvars:
        textvars[textvars.index(i)] = i.strip()

    hyprvars : List[HyprVar|None] = [None, None]
    operator_match = re.search(r"\s([\+\-\*/])\s", expression)
    if not operator_match:
        logger.error(f"hyprlang parser > couldnt determine operator at expressionession '{expression}' (this shouldn't happen)")
        return expression 

    operator = operator_match.group(1)

    succ = 0
    for i in vars:
        try:
            ind = textvars.index(i.name)
        except ValueError:
            ind = -1

        if ind == -1: 
            logger.error(f"hyprlang parser > unknown variable '{i.name}'")
            logger.debug(f"directly for the above^ > textvars: {textvars}")
            return expression 
        hyprvars[ind] = i
        succ += 1
        if succ == 2: break
    
    if None in hyprvars:
        ind = hyprvars.index(None)
        logger.error(f"hyprlang parser > unknown variable '{textvars[ind]}' at '{expression}'")
        return expression 
    
    assert hyprvars[0] is not None and hyprvars[1] is not None, "fuck the type checker, this is already checked for"

    try:
        float(hyprvars[0].val)
        float(hyprvars[1].val)
    except ValueError:
        logger.error(f"hyprlang parser > non-numeric variable in an arithmetic block ({expression} -> {{{{{hyprvars[0].val} {operator} {hyprvars[1].val}}}}})")
        return expression 

    return str(eval(f"{hyprvars[0].val} {operator} {hyprvars[1].val}"))


def _parse_hyprlang_right_comp(right : str, vars : List[HyprVar]) -> str:
    arithmetic_pattern : str = r"(?<!\\)\{\{.*?\}\}"
    arithmetic_indexes : List[tuple[int, int]] = [(m.start(), m.end()) for m in re.finditer(arithmetic_pattern, right)]
    
    bufcpy = right
    for i in arithmetic_indexes:
        expr = right[i[0]:i[1]]
        value = _unpack_arithmetic(expr, vars)
        bufcpy = bufcpy.replace(expr, value)

    
    dollar_pattern : str = r"(?<!\\)\$"
    dollar_indexes : List[int] = [m.start() for m in re.finditer(dollar_pattern, bufcpy)]
    
    newbufcpy = bufcpy
    for i in dollar_indexes:
        slice = bufcpy[i+1:]
        for var in vars:
            if slice.startswith(var.name):
                newbufcpy = newbufcpy.replace(f"${var.name}", var.val)

    right = newbufcpy
    backslash_pattern : str = r"(?<!\\)\\(?!\\)"
    backslash_indexes : List[int] = [m.start() for m in re.finditer(backslash_pattern, right)]
    c = 0
    backslash_indexes.sort()
    for i in backslash_indexes:
        right = right[:i-c] + right[i-c+1:]
        c += 1
    
    right = right.replace("\\\\", "\\") 

    return right

def parse_hyprlang_line(line : str, vars : List[HyprVar] = []) -> List[HyprVar]|HyprVar|None:
    split = line.split("=")
    
    if split[0].replace(" ", "").startswith("#hyprlangif"):
        logger.warning("hyprlang parser > 'hyprlang if' condition not supported")

    if len(split) < 2:
        return None

    left, right = split[0].strip(), "=".join(split[1:]).strip()
    
    if left == "source":
        return get_vars_from_file(os.path.expanduser(os.path.expandvars(right)))


    if left.startswith("$"):
        value = right
        if right.find("\\") != -1 or right.find("{{") != -1 or right.find("$") != -1:
            value = _parse_hyprlang_right_comp(right, vars)
        return HyprVar(left[1:].strip(), value)
    else:
        for var in vars:
            if var.name != left: continue

            value = right 
            if right.find("\\") != -1 or right.find("{{") != -1 or right.find("$") != -1:
                value = _parse_hyprlang_right_comp(right, vars)

            var.val = value
            break

    return None

def get_vars_from_file(full_fpath : str) -> List[HyprVar]:
    vars : List[HyprVar] = []
    
    f_content : List[str] = []
    with open(full_fpath, "r") as f:
        f_content = f.readlines()

    for line in f_content:
        line = line.strip()
        if not len(line): continue
        retval = parse_hyprlang_line(line, vars)
        if isinstance(retval, HyprVar):
            vars.append(retval)
        elif isinstance(retval, List):
            vars += retval

    return vars
