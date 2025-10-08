# hyprland-app-specific-keybinds
a script that allows you to have window-specific keybinds on hyprland
<details>
  <summary>installation</summary>
  
  ```sh
  git clone --depth 1 https://github.com/xeaft/hyprland-app-specific-keybinds
  cd hyprland-app-specific-keybinds
  chmod +x install.sh
  ./install.sh
  ```
\
prequisites:
- a python interpreter in PATH (either `python` or `python3`)
- `XDG_CONFIG_DIRS` and `XDG_RUNTIME_DIR` are set
- hyprland.. of course

for custom hyprland instances/dots:
- export HYPRCONF to the config folder.
  - e.g. if your config path is `~/.config/myHyprland` instead of `~/.config/hypr`, export HYPRCONF to `myHyprland` (see [env vars](https://wiki.hypr.land/Configuring/Environment-variables/))
</details>
<details>
<summary>usage</summary>
  
add `exec-once = hyprwinbinds` to your hyprland config
  
configuration:
```bind[flags] = [class], [modifiers], [key], [dispatcher], [params]```

save that into `windowkeys.conf` in your `hypr` directory\
if you want to use a different file, export `KEYCONF` to the file name (see [env vars](https://wiki.hypr.land/Configuring/Environment-variables/))

for example:
```hyprlang
bind = kitty, meta, h, exec, kitty                        # opens another kitty instance on Meta + H if kitty is focused (why would you want this)
bind = , control, space, exec, rofi -show drun            # opens rofi on CTRL + Space if a window without a class is focused (e.g. no focused window or things like some file pickers)

# whitespace doesnt matter, examples below are valid:
bind=,control,space,exec,rofi -show drun
bind  =    , control  , space   ,exec ,rofi -show drun

# or with bind flags
binderl = kitty, meta, e, notify-send "notification" "some notif"
```

to stop hyprwinbinds: \
`hyprwinbinds stop`\
to reload the config (it doesnt reload automatically like hyprland (soon))\
`hyprwinbinds reload`
</details>
<details>
  <summary>not (yet) supported things</summary>

  - live reloading
  - other ways of specifying a window (aside from its class)
</details>

