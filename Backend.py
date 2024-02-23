from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_connection_string'
db = SQLAlchemy(app)

#testtesttest
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tokens = db.Column(db.Integer, default=0)

# Quest model
class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

# API endpoint for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    # Create a new user
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# API endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Find the user by username
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({'message': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful', 'user_id': user.id}), 200

# API endpoint for creating a new quest
@app.route('/quests', methods=['POST'])
def create_quest():
    data = request.get_json()
    title = data['title']
    description = data['description']

    new_quest = Quest(title=title, description=description)
    db.session.add(new_quest)
    db.session.commit()

    return jsonify({'message': 'Quest created successfully', 'quest_id': new_quest.id}), 201

# API endpoint for awarding tokens to a user
@app.route('/award_tokens', methods=['POST'])
def award_tokens():
    data = request.get_json()
    user_id = data['user_id']
    tokens = data['tokens']

    user = User.query.get(user_id)
    user.tokens += tokens
    db.session.commit()

    return jsonify({'message': 'Tokens awarded successfully'}), 200

if __name__ == '__main__':
    app.run()