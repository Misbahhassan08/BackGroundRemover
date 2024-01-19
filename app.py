from flask import Flask, render_template, request, Response, jsonify, send_file
from pygtail import Pygtail
import logging, os, sys, time
from flask_socketio import SocketIO,emit
from flask_cors import CORS, cross_origin
import os
from PIL import Image
import io
import base64
from config import *
import logging
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
CORS(app)


image = None

LOG_FILE = 'app.log'
log = logging.getLogger('__name__')
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

class MyDataBase:
    def __init__(self):
        self.connection = pymysql.connect(host='74.50.90.186',
                      user='technove_misbah',
                      password='i3kMKJ&T29Np',
                      db='technove_demo',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)
        pass # End of MyDataBase class

    def insertToDB(self, query, values, table_name):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query, values)
        self.cursor.connection.commit()
        self.cursor.execute(f""" SELECT * from {table_name}""")
        output = self.cursor.fetchall()
        data = None
        for i in output:
            data = i
        self.cursor.close() # Closing the cursor
        return data # end of insertToDB function
    
    def fetchData(self,query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        self.cursor.connection.commit()
        output = self.cursor.fetchall()
        self.cursor.close() #Closing the cursor
        return output # end of fetchTableData function
    
    def deleteData(self,query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        self.cursor.connection.commit()
        self.cursor.close() #Closing the cursor
        pass

def logUpdater(mesg):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.info('{}'.format(mesg))
        pass

def print_custom_message(msg):
    if is_console:
        print(f"SERVER:{msg}")
    pass




@app.route("/", methods=["GET"])
def on_get_default():
    return jsonify({"Status":"OK"})

@app.route('/log')
def progress_log():
	def generate():
		for line in Pygtail(LOG_FILE, every_n=0):
			yield "->" + str(line) + "\n\n"
			
	return Response(generate(), mimetype= 'text/event-stream')

# -------------------------------- Receive Key API ------------------------#
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

@app.route("/")
def init_page():
     return jsonify({"Status" : "API Health 100%"})

@app.route("/receivekey", methods=["POST"])
def receive_key():
    print('Receive key api called !!!')
    global image
    db = MyDataBase()
    tableName = "bg_tbl"
    if request.method == "POST":

        # Extract data to from json
        jsonData = request.get_json()
        random_key_string = jsonData["text"]

        # Fetch data to from Database
        query = f""" SELECT * from {tableName} WHERE KeyValue={random_key_string}"""
        rowData = db.fetchData(query)
        original_image = rowData["Image"] # Image in  base 64 string
        bgImage = rowData["bg_image"] # Image in  base 64 string
        key, Status = rowData["KeyValue"], rowData["Status"]
        logUpdater("Found the Image from Local AI server")

        # Delete data to from Database of current KeyValue of row
        query = f"""DELETE FROM {tableName} WHERE KeyValue = {key}"""
        db.deleteData(query)
        return jsonify({"image": bgImage})


# -------------------------------- Remove API -----------------------------#
# ------------------------------------------------------------------------ #
# ------------------------------------------------------------------------ #

@app.route("/remove", methods=["POST"])
def remove():
    print('Remove api called !!!')
    db = MyDataBase()
    tableName = "image_tbl"
    Status = 0
    if request.method == "POST":

        # Extract data to from json
        jsonData = request.get_json()
        base64_image_string, random_key_string = jsonData["file"], jsonData["text"]

        # Save data to database
        query  =  (f"""INSERT INTO image_tbl (KeyValue, Image, Status)  VALUES (%s, %s, %s)""")
        values = (random_key_string,base64_image_string,Status)
        lastRow = db.insertToDB(query, values,tableName)
        image_id = lastRow["IMAGEID"]
        
        # Save progress in log file
        logUpdater(f"New Record with image ID : ({image_id}) Save in DataBase")
    return jsonify({"Status":"OK"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)

