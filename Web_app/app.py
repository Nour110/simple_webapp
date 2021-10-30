# export FlASK_ENV = development
# flask run

from flask import Flask, render_template, request, g
import sqlite3

def get_message_db():
	if 'message_db' not in g:
		g.message_db = sqlite3.connect('message_db.sqlite')
	g.message_db = sqlite3.connect("message_db.sqlite")
	curr = g.message_db.cursor()
	curr.execute("CREATE TABLE IF NOT EXISTS messages (id,handle,message)")
	g.message_db.commit()

	return g.message_db

def insert_message(request):
	db = get_message_db()
	curr = db.cursor()
	msg = request.form['message']
	name = request.form['name']
	number = curr.execute("SELECT COUNT(1) FROM messages").fetchone()[0]
	number = number+1
	cmd = "INSERT INTO messages (id,handle,message) VALUES (:num,:nme,:mess)"
	key = {"num":number,"nme":name,"mess":msg}
	curr.execute(cmd,key)
	db.commit()
	return

app = Flask(__name__)

@app.route("/")
def main():
	return render_template("main.html")


@app.route("/submit/", methods= ["POST","GET"])
def submit():
	if request.method == "GET":
		return render_template("submit.html")
	if request.method == "POST":
		insert_message(request)
		return render_template("submit.html", thanks = True)
