from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from config import Config
from routes import chat_bp
from socket_events import init_socket_events  # Import the function
import logging
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, ActionHub

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)  
socketio = SocketIO(app)

app.register_blueprint(chat_bp, url_prefix='/chat')

# Initialize socket events
init_socket_events(socketio)

@app.route('/')
def home():
    return render_template('home.html')  # Render the combined home page

@app.route('/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    return '<br>'.join(routes)

@app.route('/test')
def test():
    return "CORS is working!"

def get_report_by_id(report_id):
    return db.session.query(ActionHub).filter_by(ah_report_id=report_id).first()

if __name__ == '__main__':
    socketio.run(app)  #, debug=True