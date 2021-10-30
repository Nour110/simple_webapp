# export FlASK_ENV = development
# flask run

# Imports
from flask import Flask, render_template, request, g
import sqlite3

# This function will create a new database unless one already exists.
# it will return a connection to the database
def get_message_db():
	# check if the database does not exist. If it doesn't then create it and return a connection to it
	if 'message_db' not in g:
		g.message_db = sqlite3.connect("message_db.sqlite")
		curr = g.message_db.cursor()
		curr.execute("CREATE TABLE IF NOT EXISTS messages (id,handle,message)")
		# we must commit to esnure our table has been added
		g.message_db.commit()
		return g.message_db

	# Create a connection to the database then return the connection
	g.message_db = sqlite3.connect("message_db.sqlite")
	return g.message_db


# function to insert a new row into the database
def insert_message(request):
	# first we establish a connection to the database using our previous function
	db = get_message_db()
	curr = db.cursor()

	# we pull the user inputted info from request
	msg = request.form['message']
	name = request.form['name']

	# extract the total number of rows in the database
	number = curr.execute("SELECT COUNT(1) FROM messages").fetchone()[0]
	# add 1 to that value
	number = number+1

	# insert the row with the correct id#, handle and message
	cmd = "INSERT INTO messages (id,handle,message) VALUES (:num,:nme,:mess)"
	key = {"num":number,"nme":name,"mess":msg}
	curr.execute(cmd,key)
	# commit to make sure we inserted the row and close our connection
	db.commit()
	db.close()
	# return
	return

# function to pull n random messages from the database
def random_message(n):
	# establish a connection to the database using our previous function
	db = get_message_db()
	curr = db.cursor()

	# check if there are enough messages, otherwise we'll display all the messages
	number = curr.execute("SELECT COUNT(1) FROM messages").fetchone()[0]
	if n > number:
		n = number

	# pull the messages and the handles from the database and save them to output	
	cmd = "SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT "+str(n)
	output = curr.execute(cmd).fetchall()
	# close our connection to the database
	db.close()
	# returns a list of tuples, with the first element of each tuple being the handle
	# the second element of each tuple is the message
	return output


# initialize our webapp
app = Flask(__name__)

# define and load the main page of our webapp
@app.route("/")
def main():
	return render_template("main.html")

# handle the submission of user input and call the insert_message function to save it to our database
@app.route("/submit/", methods= ["POST","GET"])
def submit():
	if request.method == "GET":
		return render_template("submit.html")
	else: 
		insert_message(request)
		return render_template("submit.html", thanks = True)


@app.route("/view/")
def view():
	display = random_message(7)
	return render_template("view.html",messages = display)
