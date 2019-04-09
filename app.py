import json
import os
import time
from flask import *
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect mongodb database
db_client = MongoClient("mongodb://127.0.0.1:27017")
db = db_client["tori"]
collec = db["todos"]


# Render template of root
@app.route("/")
def show_todos():
    todo_list = list(collec.find().sort("created_time", 1))
    return render_template('todo.html', todo_list=todo_list)

# Create a new todo item
@app.route('/todos', methods=['POST'])
def new_todo():
    # check if the content is empty
    if ''.join(request.form['content'].split(' ')) == '':
        return redirect(url_for('show_todos'))

    now = time.time()
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
    content = {
        "content": request.form['content'],
        "created_time": format_time,
        "updated_time": format_time
        # "rank": 
    }
    collec.insert_one(content)
    return redirect(url_for('show_todos'))

# Delte a todo item
@app.route('/todos/delete/<string:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    collec.delete_one({'_id': ObjectId(todo_id)})
    return redirect(url_for("show_todos"))

# Update a todo item
@app.route('/todos/update/<string:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    if request.method == "POST":
        # check if the content is empty
        if ''.join(request.form['content'].split(' ')) == '':
            return redirect(url_for("show_todos"))
        now = time.time()
        format_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
        updated_content = {
            "content": request.form['content'],
            "updated_time": format_time
        }
        collec.update_one({'_id': ObjectId(todo_id)}, {"$set": updated_content})
        return redirect(url_for("show_todos"))
    elif request.method == "GET":
        item = collec.find_one({'_id': ObjectId(todo_id)})
        return render_template('edit.html', item=item)

