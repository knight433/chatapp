from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from databaseCon import init, userData, Messages, Groups
import emotionClassify
import SummaryText
from autoComplete import NextWord

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

global userObj
global msgObj
global grpObj
global sumup
global emotion
global next_word_predictor

init()
userObj = userData()
msgObj = Messages()
grpObj = Groups()
sumup = SummaryText.Summary()
emotion = emotionClassify.EmotionClassifier()
next_word_predictor = NextWord()

chat_messages = []

@app.route('/get-messages', methods=['GET'])
def get_messages():
    return jsonify({"messages": chat_messages})

@socketio.on('message')
def handle_message(data):
    username = data.get('username')
    message = data.get('message')
    full_message = f"{username}: {message}"
    chat_messages.append(full_message)
    send(full_message, broadcast=True)

@socketio.on('login')
def handle_login(data):
    username = data.get('username')
    password = data.get('password')

    auth = userObj.loginAuth(username, password)
    
    if auth[0]:
        emit('login_response', {'status': 'success', 'username': username})
    else:
        emit('login_response', {'status': 'error', 'message': auth[1]})

@socketio.on('GetGroups')
def get_groups(data):
    username = data.get('username')
    if username:
        listOfGroups = grpObj.getGroup(username)
        emit('GroupsList', listOfGroups)
    else:
        emit('GroupsList', [])

@socketio.on('GetGroupMessages')
def get_messages(data):
    user = data.get('username')
    group = data.get('groupid')

    mesg = msgObj.loadGroupMessages(user, group)
    emit('messages', mesg)

@socketio.on('SendMessage')
def send_message(data):
    user = data.get('username')
    msg = data.get('message')
    grpId = data.get('group_id')

    msgObj.message(user, grpId, msg)
    emit('new_message', {'user': user, 'content': msg, 'group_id': grpId}, broadcast=True)

@socketio.on('messagesForSummary')
def get_summary(data):
    messages = data.get('messages')
    print('got messages:', messages)
    summatized_text = sumup.get_summary(messages)
    print(summatized_text)

    emit('summarized_text', summatized_text)

@socketio.on('emotionClassifier')
def get_emotions(data):
    messages = data.get('messages')
    print('got message', messages)
    emo = emotion.emoWhat(messages)

    emit('emotion', emo)

@socketio.on('signup')
def sign_up(data):
    username = data.get('username')
    password = data.get('password')

    added = userObj.addUser(username, password)

    if added:
        emit('login_response', {'status': 'success'})
    else:
        emit('login_response', {'status': 'error', 'message': 'Invalid username or password'})

@socketio.on('predict_next_word')
def predict_next_word(data):
    text = data.get('text')
    next_words = next_word_predictor.nextWords(text, top_k=3)
    emit('next_word', {'next_words': next_words})

if __name__ == '__main__':
    socketio.run(app)
