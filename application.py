from random import random
from time import sleep

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread, Event

app = Flask(__name__)
app.config['SECRET_KEY'] = '1222234344444'
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()


class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        print("Making random numbers")
        while not thread_stop_event.isSet():
            number = round(random() * 10, 3)
            print(number)
            socketio.emit('newnumber', {'number': number}, namespace='/test')
            sleep(self.delay)

    def run(self):
        self.randomNumberGenerator()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    print('Client connected')

    if not thread.is_alive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()


if __name__ == "__main__":
    socketio.run(app)
