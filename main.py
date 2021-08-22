import os
import socket
from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from rtmidi import midiconstants as midi
import rtmidi
from dotenv import dotenv_values, load_dotenv
import webbrowser
import qrcode

load_dotenv('.env')
settings = dotenv_values(".settings")
app = Flask(__name__, static_url_path='/{}'.format(settings['CLIENT_BASE_DIR']))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

device = rtmidi.MidiOut()
midi_ports = device.get_ports()


try:
    device.open_virtual_port(settings['MIDI_NAME'])
except NotImplementedError:
    try:
        name = list(filter(lambda n: n.startswith(settings['MIDI_NAME']), midi_ports))[0]
        num = midi_ports.index(name)
        device.open_port(num)
    except IndexError:
        exit("Please run loopMIDI first")
    
    

io = SocketIO(app)

ip = socket.gethostbyname(socket.gethostname())
port = settings['SERVER_PORT']


@io.on('note_on')
def send_note_on(data):
    global device
    device.send_message([midi.NOTE_ON+data['channel'], data['note'], data['velocity']])

@io.on('note_off')
def send_note_off(data):
    global device
    device.send_message([midi.NOTE_OFF+data['channel'], data['note'], data['velocity']])

@io.on('all_note_off')
def send_all_note_off(data):
    global device
    device.send_message([midi.CONTROLLER_CHANGE+data['channel'], midi.ALL_NOTES_OFF, 0])

@io.on('cc')
def send_cc(data):
    global device
    device.send_message([midi.CONTROLLER_CHANGE+data['channel'], data['control'], data['value']])

@app.route('/')
def base():
    return send_from_directory(settings['CLIENT_BASE_DIR'], 'index.html')

@app.route('/<path:path>')
def home(path):
    return send_from_directory(settings['CLIENT_BASE_DIR'], path)

if __name__ == "__main__":
    if settings['CLIENT_BASE_DIR'] == 1:
        url = 'http://{}:{}/'.format(ip, port)
        qrCode = qrcode.make(url)
        try:
            qrCode.save("url.png")
        except OSError:
            os.remove("url.png")
            qrCode.save("url.png")
        webbrowser.open_new("url.png")

    io.run(app, host=ip, port=port)