from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

groceries = []
print(groceries)
app = Flask(__name__)
#CORS(app)
app.config['SECRET_KEY'] = 'secret!'
#app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

@app.route('/')
def index():
    return ('<h1>This is the index page of the server that is serving KauppaLista</h1>')

@socketio.on('connect')
def handle_connection():
    print('moi yhteys')
    emit('FromAPI', groceries)

@socketio.on('adding-grocery')
def handle_message(message):
    print('moi')
    print('received message: ' + message)
    groceries.append(message)
    print(groceries)
    emit('AfterAdding', groceries, broadcast=True)

@socketio.on('deleting-grocery')
def handle_deleting(message):
    print('to be deleted: ' + message)
    groceries.remove(message)
    print(groceries)
    emit('AfterDeleting', groceries, broadcast=True)

@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print(e)

if __name__ == '__main__':
    socketio.run(app, debug=True)
    print('Listening on port ')