# What ?

This application has been developed to be used as an [OBS](https://obsproject.com/) overlay to add volleyball score to streaming.
It isn't well written, the code is pretty dumb and naive but it gets the job done.

It uses socket.io and the broacast mode : any changes made in the `remote` or `setup` page will update the values on any client.

# Installation

## Ubuntu
```shell
./scripts/install.sh
```

If you want to add a desktop shortcut :
```shell
./scripts/ubuntu.sh
```

## Other Linux & MacOS and probably Windows
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Run the application
```shell
./scripts/start.sh
```

Or
```
python3 main.py
```

Alternative to disable debug for production :
```
python3 main.py --debug-off
```

# Usage
## Setup / logos
The `/setup` page allows you to set the team name and logo or team color.
If one of the team logo is set to `None` then the colors will be used for both teams.
jpg / png / svg logo files must be located in the `static/logos` directory.

The `New Game` button will reset scores, keeping teams' names, logos and colors.

## Remote
The main part of the application is the `/remote` page where you can manage the score.

## Score
The `score`only shows the current score. It's basically the page to be used in OBS

# Thanks
Many many thanks to [tchoupinax](https://github.com/tchoupinax) and [lilipix](https://github.com/lilipix) for their help & support !
