# hyprland-app-specific-keybinds
script that allows you to have keybinds for specific windows on hyprland
<details>
  <summary>installation</summary>
  
  ```sh
  git clone --depth 1 https://github.com/xeaft/hyprland-app-specific-keybinds
  cd hyprland-app-specific-keybinds
  chmod +x install.sh
  ./install.sh
  ```
</details>
<details>
<summary>usage</summary>
  
`exec-once = hyprwinbinds` or the path to it, if its not in PATH
  
configuration:
```bind = [class], [modifiers], [key], [dispatcher], [params]```

save that into `windowkeys.conf` in your `hypr` directory

For example:
```hyprlang
bind = kitty, meta, h, exec, kitty                        # opens another kitty instance on Meta + H if kitty is focused (why would you want this)
bind = , control, space, exec, rofi -show drun            # opens rofi on CTRL + Space if a window without a class is focused (e.g. no window whatsoever or things like some file pickers)

# whitespace doesnt matter, examples below are valid:
bind=,control,space,exec,rofi -show drun
bind  =    , control  , space   ,exec ,rofi -show drun
```

to stop hyprwinbinds: \
`hyprwinbinds stop`\
to reload the config (it doesnt reload automatically like hyprland (soon))\
`hyprwinbinds reload`
</details>
