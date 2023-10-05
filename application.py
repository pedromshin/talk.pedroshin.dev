from flask_socketio import SocketIO, emit
from flask import Flask, session

application = Flask(__name__)
socketio = SocketIO(application, async_mode=None, cors_allowed_origins="*")

response_event = "response_to_frontend"

messages = []

@socketio.on("new_message")
def new_message(message):
    session["new_message"] = session.get("new_message", 0) + 1

    print(f"New message received: {message}")
    
    # Add the new message to the messages array
    messages.append(message['message'])
    
    # Emit a response to the frontend with the updated messages array and count
    emit("response_to_frontend", {'message': message['message']}, broadcast=True)

@socketio.on('connect')
def connect():
    emit("response_to_frontend", {'message': "hello"}, broadcast=True)

if __name__ == '__main__':
    socketio.run(application, host='0.0.0.0', port=5000, debug=True)