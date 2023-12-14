from flask import Flask, request, send_file, jsonify
from flask_socketio import SocketIO,emit
from flask_cors import CORS, cross_origin
import os
from PIL import Image
import io
import base64
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '98kjhkjhkj'


socketio = SocketIO(app, cross_origin='*')

image = None


@socketio.on('connect')
def on_connect():
    global image
    image = None 
    print('Server received connection')
    socketio.send("client connect")

@socketio.on('pong')  
def on_pong(msg):
    print("received pong"+msg) 
    socketio.emit('ping',"ping from server ")
    pass 


def print_custom_message(msg):
    if is_console:
        print(f"SERVER:{msg}")
    pass

@socketio.on('message')
def message(data):
    global image
    image = data
    print("data received from client")  # show msg from client
    #emit('response', {'from': 'server'})
    
    pass


@app.route("/remove", methods=["POST"])
def remove():
    global image
    if 'file' not in request.files:
        return jsonify({'error': 'missing file'}), 400

    if request.files['file'].filename.rsplit('.', 1)[1].lower() not in ["jpg", "png", "jpeg"]:
        return jsonify({'error': 'invalid file format'}), 400

    data = request.files['file'].read()
    
    if len(data) == 0:
        return jsonify({'error': 'empty image'}), 400
    
    base64_data = base64.b64encode(data).decode('utf-8')
    _dict = {
        "image":str(base64_data)
    }
    new_image = None

    print("SERVER: Data emitting ...")
    socketio.emit('response1',  _dict)

    while True:
        if image is not None:
            new_image = image
            break       
        pass

    image = None
    print("SERVER: DATA FOUND")
    _dict["image"] = new_image
    return jsonify(_dict)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=port)
