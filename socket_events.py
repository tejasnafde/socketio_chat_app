from flask_socketio import emit, join_room
from flask import request, session
from models import ActionHub, User
from datetime import datetime
from models import db
import json

def init_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('send_message')
    def handle_send_message(data):
        # Ensure the message data is valid
        if 'report_id' not in data or 'content' not in data:
            emit('error', {'message': 'Invalid message data'})
            return
        
        # Get user from session or data
        user_id = session.get('user_id', data.get('user_id', 1))
        username = session.get('username', 'Anonymous')
        
        # Create a new message entry in the database
        new_message = ActionHub(
            ah_type='message',
            ah_report_id=data['report_id'],
            ah_user_id=user_id,
            ah_content={
                'message': data['content'],
                'username': username,
                'timestamp': datetime.utcnow().isoformat()
            },
            ah_created_at=datetime.utcnow()
        )
        
        # Save the message to the database
        db.session.add(new_message)
        db.session.commit()
        
        # Prepare message for broadcast
        message_data = {
            'ah_id': new_message.ah_id,
            'ah_user_id': new_message.ah_user_id,
            'ah_content': {
                'message': data['content'],
                'username': username,
                'timestamp': datetime.utcnow().isoformat()
            },
            'ah_created_at': datetime.utcnow().isoformat()
        }
        
        # Emit the new message to all clients in the room
        emit('new_message', message_data, room=data['report_id'])

    @socketio.on('join_room')
    def handle_join_room(data):
        report_id = data['report_id']
        join_room(report_id)
        messages = ActionHub.query.filter_by(ah_report_id=report_id, ah_type='message').all()
        
        message_list = []
        for msg in messages:
            user = User.query.get(msg.ah_user_id)
            username = user.username if user else 'Anonymous'
            
            # Parse message content
            try:
                # Handle both string and dict formats
                content = msg.ah_content
                if isinstance(content, str):
                    content = json.loads(content)
            except:
                content = {'message': str(content)}

            # Ensure proper structure
            message_data = {
                'ah_id': msg.ah_id,
                'ah_user_id': msg.ah_user_id,
                'ah_content': {
                    'message': content.get('message', ''),
                    'username': content.get('username', username),
                    'timestamp': content.get('timestamp', msg.ah_created_at.isoformat())
                },
                'ah_created_at': msg.ah_created_at.isoformat()
            }
            
            message_list.append(message_data)
        
        emit('message_history', message_list, room=request.sid)