#!/bin/bash

BASEPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; cd ..; pwd -P )"
cd $BASEPATH


source ~/.config/user-dirs.dirs

desktop_file=$XDG_DESKTOP_DIR/volley-scoreboard.desktop

cat <<EOF > $desktop_file
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Terminal=true
Exec=$BASEPATH/scripts/start.sh
Name=Volley Scoreboard
Icon=$BASEPATH/static/volley.png

EOF

chmod +x $desktop_file
