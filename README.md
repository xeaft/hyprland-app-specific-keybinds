# hyprland-app-specific-keybinds
A script that allows you to have window-specific keybinds on hyprland

## Table of Contents
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [Commands](#commands)
- [Configuration](#configuration)
  - [Examples](#examples)

## Installation
  ```sh
  git clone --depth 1 https://github.com/xeaft/hyprland-app-specific-keybinds
  cd hyprland-app-specific-keybinds
  chmod +x install.sh
  ./install.sh
  ```

#### Prerequisites:
- a python interpreter in PATH (either `python` or `python3`)
- `XDG_CONFIG_HOME` and `XDG_RUNTIME_DIR` are set
- the `pyinotify` python module (`sudo pacman -S --needed python-pyinotify` on arch)

for custom hyprland instances/dots:
- export HYPRCONF to the config folder.
  - e.g. if your config path is `~/.config/myHyprland` instead of `~/.config/hypr`, export HYPRCONF to `myHyprland` (see [env vars](https://wiki.hypr.land/Configuring/Environment-variables/))

## Usage
- add this to your hyprland config
  ```ini
  exec-once = hyprwinbinds
  ```
        
#### Commands:
to stop hyprwinbinds: \
`hyprwinbinds stop`\
to reload the config (it reloads automatically (assuming `pyinotify`), but if you need this):\
`hyprwinbinds reload`

  
## Configuration:

> [!NOTE]
> Selectors are space-separated, put selectors with spaces into brackets (as shown below)

> [!WARNING]
> All selectors must be exactly matched (Kitty != kitty)

Supported keywords:\
```ini
bind[flags] = [selectors], [modifiers], [key], [dispatcher], [params}
unbind = [selectors], [modifiers], [key], [dispatcher], [params]
source = [file_path] # this ONLY sources variables, NOT binds\
$new_var = [value]
existing_var = [value]
$new_var = {{existing_var [+,/,-,*] existing_var2}}
```
variable syntax according to [hyprlang](https://wiki.hypr.land/Hypr-Ecosystem/hyprlang/#defining-variables)

save that into `windowkeys.conf` in your `hypr` directory\
if you want to use a different file, export `KEYCONF` to the file name (see [env vars](https://wiki.hypr.land/Configuring/Environment-variables/))

> [!NOTE]
> **Not** all windowrule selectors from [the wiki](https://wiki.hypr.land/Configuring/Window-Rules/) are supported. You can only use selectors available in `hyprctl clients`

#### Examples:
```ini
source = ~/.config/hypr/hyprland.conf                             # recursively loads variables from hyprland.conf
$menu = rofi -show drun

bind = class:kitty, meta, h, exec, kitty                          # opens another kitty instance on Meta + H if kitty is focused
bind = , control, space, exec, $rofi                              # opens rofi (value of $menu) on CTRL + Space if no window is focused
unbind = class:(), control, space, exec, rofi -show drun          # opens rofi on CTRL + Space if a window with any class is focused
bind = fullscreen:1 xwayland:0, meta, g, killactive               # kills a window on Meta + G if its a native window in fullscreen
bind = title:(App with a multi-word title), , space, killactive   # kills a window on Space if it has that exact title
unbind = class:(.*tty.*), meta, d, killactive                     # kills the window on Meta + G if its class does not contain "tty" (e.g. kitty, alactritty)

# whitespace doesnt matter, examples below are valid:
bind=,control,space,exec,rofi -show drun
bind  =    , control  , space   ,exec ,rofi -show drun

# or with bind flags
binderl = class:kitty, meta, e, notify-send "notification" "some notif"
```


