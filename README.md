# hyprland-app-specific-keybinds

usage:
`exec-once = hyprwinbinds # or the path to it, if its not in PATH`

configuration:
```bind = [class], [modifiers], [key], [dispatcher], [params]```

save that into `windowkeys.conf` in your `hypr` directory

For example:
```hyprlang
bind = kitty, meta, h, exec, kitty # opens another kitty instance on Meta + H if kitty is focused (why would you want this)
bind = , control, space, exec, rofi -show drun # opens rofi on CTRL + Space if a window without a class is focused (e.g. no window whatsoever or things like some file pickers)```
