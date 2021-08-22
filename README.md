## Introduction
midi-socket-server is a flask app that can be used as a midi server using [web socket](https://pypi.org/project/Flask-SocketIO/) and [rtmidi](https://pypi.org/project/python-rtmidi/)

<hr>

## Installation
>required python

```bash
python -m venv env

env/scripts/activate

pip istall -r requirements.txt
```

<hr>

## Preparation
>Windows required [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) to be installed

### For Windows Only
open loopMIDI and create a new port and in ***.settings*** change **MIDI_NAME** variable with the same name as the port name 

```bash
#.settings

MIDI_NAME="Your loopMIDI Port"
```

### For All System
change **CLIENT_BASE_DIR** in ***.settings*** to public directory of [midi-socket-layout](https://github.com/fmented/midi-socket-layout) 

```bash
#.settings

CLIENT_BASE_DIR="../path/to/layout/directory"
```

you can also change server port if you need to
```bash
#.settings

SERVER_PORT=8080
```

lastly, create ***.env*** file in root directory
and add **SECRET_KEY** and **FLASK_ENV** variables
```bash
#.env

FLASK_ENV="development"
#development or production

SECRET_KEY="add your secret key here"
```

<hr>

## Start
to start the server run
```bash
python main.py
```
it will show a qrcode that can be scanned by other device that is in the same network to act as a MIDI contoller
if you find the qrcode is annoying, you can turn it off in ***.settings*** in **SHOW_QR** variable 