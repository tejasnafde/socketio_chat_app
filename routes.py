from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from models import db, ActionHub, User
from utils import get_user_by_id, get_report_by_id, get_section_by_id
import random
from datetime import datetime

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/create', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        room_name = request.form.get('room_name', f"Room-{random.randint(1000, 9999)}")
        
        if not user_name:
            return redirect(url_for('home'))
        
        # Check if user exists, if not create one
        user = User.query.filter_by(username=user_name).first()
        if not user:
            user = User(username=user_name)
            db.session.add(user)
            db.session.commit()
        
        # Store user ID in session
        session['user_id'] = user.id
        session['username'] = user.username
        
        # Generate a unique report ID
        report_id = random.randint(1000, 9999)
        
        # Create a new ActionHub entry for the room
        new_room = ActionHub(
            ah_type='room',
            ah_report_id=report_id,
            ah_user_id=user.id,
            ah_content=room_name,
            ah_created_at=datetime.utcnow(),
            ah_status=1
        )
        
        # Add the new room to the database
        db.session.add(new_room)
        db.session.commit()
        
        # Redirect to the chat page with the new report_id
        return redirect(url_for('chat.chat_page', report_id=report_id))
    
    # If GET request, redirect to home
    return redirect(url_for('home'))

@chat_bp.route('/join', methods=['GET'])
def join_room():
    user_name = request.args.get('user_name')
    report_id = request.args.get('report_id')
    
    if not user_name or not report_id:
        return redirect(url_for('home'))
    
    # Check if user exists, if not create one
    user = User.query.filter_by(username=user_name).first()
    if not user:
        user = User(username=user_name)
        db.session.add(user)
        db.session.commit()
    
    # Store user ID in session
    session['user_id'] = user.id
    session['username'] = user.username
    
    # Check if room exists
    room = ActionHub.query.filter_by(ah_report_id=report_id, ah_type='room').first()
    if not room:
        # Room doesn't exist, redirect to home with error
        return redirect(url_for('home'))
    
    # Redirect to the chat page with the report_id
    return redirect(url_for('chat.chat_page', report_id=report_id))

@chat_bp.route('/chat/<int:report_id>', methods=['GET'])
def chat_page(report_id):
    # Check if user is in session
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    # Get room information
    room = ActionHub.query.filter_by(ah_report_id=report_id, ah_type='room').first()
    if not room:
        return redirect(url_for('home'))
    
    # Get room name from the room's ah_content
    room_name = room.ah_content
    
    # Fetch existing messages for the chat room
    messages = ActionHub.query.filter_by(ah_report_id=report_id, ah_type='message').all()
    
    return render_template('index.html', report_id=report_id, room_name=room_name, messages=messages)