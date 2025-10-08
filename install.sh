#!/bin/sh

sudo tee /usr/bin/hyprwinbinds <<EOF
#!/bin/sh
exec $(pwd)/hyprwinbinds "\$@"
EOF

sudo chmod a+x /usr/bin/hyprwinbinds
