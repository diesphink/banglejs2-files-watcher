# banglejs2-files-watcher
Monitor file changes and upload to bangle.js2, sending files to storage and reloading application

# Installation

Installing requirements:
```sh
pip3 i -r requirements.txt
```

Installing requirements with virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

# Usage

```
usage: watcher.py [-h] [--buffer_size BUFFER_SIZE] [--exec EXEC] [-v] address file [file ...]

Bangle Watcher

positional arguments:
  address               bluetooth address to connect
  file                  files to watch

optional arguments:
  -h, --help            show this help message and exit
  --buffer_size BUFFER_SIZE
                        buffer size (default 20)
  --exec EXEC           script to run (load) after each upload
  -v, --verbose         verbosity: -v show response from bangle, -vv show all DEBUG logs
```

# Usage example

For a few files for my current clock app (sphclock at the moment):

- **sphclock.info**: json with app information
- **sphclock.fonts.js**: js with only the setFont functions
- **sphclock.background.js**: js with only the image function
- **sphclock.app.js**: js with the core clock application

For this setup, I start the monitor with:

```sh
$ python watcher.py 'aa:bb:cc:dd:ee:ff' ../sphclock/sphclock.* --exec sphclock.app.js -v
2022-01-03 19:46:43 - Connecting to aa:bb:cc:dd:ee:ff...
2022-01-03 19:46:45 - Connected
2022-01-03 19:46:45 - Resetting
2022-01-03 19:46:45 - Disabling echo
2022-01-03 19:46:46 - Sending ../sphclock/sphclock.app.js...
2022-01-03 19:46:48 - ../sphclock/sphclock.app.js sent!
2022-01-03 19:46:48 - Sending ../sphclock/sphclock.background.js...
2022-01-03 19:46:49 - ../sphclock/sphclock.background.js sent!
2022-01-03 19:46:49 - Sending ../sphclock/sphclock.fonts.js...
2022-01-03 19:46:58 - ../sphclock/sphclock.fonts.js sent!
2022-01-03 19:46:58 - Sending ../sphclock/sphclock.info...
2022-01-03 19:46:58 - ../sphclock/sphclock.info sent!
2022-01-03 19:46:58 - Executing sphclock.app.js...
2022-01-03 19:46:58 - 
 ____                 _ 
|  __|___ ___ ___ _ _|_|___ ___ 
|  __|_ -| . |  _| | | |   | . |
|____|___|  _|_| |___|_|_|_
2022-01-03 19:46:58 - |___|
         |_| espruino.com
 2v11 (c) 2021 G.Williams


2022-01-03 19:46:59 - >

```