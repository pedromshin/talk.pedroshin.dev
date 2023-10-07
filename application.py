from flask_socketio import SocketIO, emit
from flask import Flask, session, request

application = Flask(__name__)
socketio = SocketIO(application, async_mode=None, cors_allowed_origins="*")

response_event = "response_to_frontend"

messages = []
active_clients = set()

@socketio.on("new_message")
def new_message(message):
    session["new_message"] = session.get("new_message", 0) + 1

    print(f"New message received: {message}")
    
    # Add the new message to the messages array
    messages.append(message['message'])
    
    # Emit a response to the frontend with the updated messages array and count
    emit("response_to_frontend", {'message': message['message'], 'username': message['username']}, broadcast=True)


@socketio.on("connect")
def connect():
    # Access the client's unique identifier (SID)
    client_sid = request.sid
    
    # Check if the client is not already in the set (i.e., a new connection)
    if client_sid not in active_clients:
        active_clients.add(client_sid)
    
    emit("connections_update", {'message': f"New user connected. Total connections: {len(active_clients)}", 'connections': len(active_clients)}, broadcast=True)

@socketio.on("disconnect")
def disconnect():
    # Access the client's unique identifier (SID)
    client_sid = request.sid
    
    # Check if the client is in the set (i.e., an existing connection)
    if client_sid in active_clients:
        active_clients.remove(client_sid)
    
    emit("connections_update", {'message': f"User disconnected. Total connections: {len(active_clients)}", 'connections': len(active_clients)}, broadcast=True)

if __name__ == '__main__':
    socketio.run(application, host='0.0.0.0', port=5000, debug=True)