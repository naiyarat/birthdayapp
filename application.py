import os
import re
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application

app = Flask(__name__)

db = SQL("sqlite:///birthday.db")

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # error checking
        if not request.form.get("username") or not request.form.get("password"):

            flash("Please enter a username and/or password", "danger")

            return redirect("/register")

        elif len(db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))) != 0:

            flash("This user name already exists","danger")

            return redirect("/register")

        # check if passwords match
        elif request.form.get("password") != request.form.get("confirmation"):

            flash("The passwords do not match", "danger")

            return redirect("/register")

        # check if passwords has numbers and letters in it
        elif request.form.get("password").isdigit() == True or request.form.get("password").isalpha() == True:

            flash("Please include at least 8 numbers and alphabets in your password", "danger")

            return redirect("/register")

        # check if password is 8 letters
        elif len(request.form.get("password")) < 8:

            flash("Please include at least 8 numbers and alphabets in your password", "danger")

            return redirect("/register")

        # no errors
        else:

            # generate password hash
            password_hash = generate_password_hash(request.form.get("password"))

            #if username is and password is usable and matches with confirmation, insert it into users database
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), password_hash)

            return redirect("/login")

    # user reached route via GET
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # user reached route via POST
    if request.method == "POST":

        # check for errors
        if not request.form.get("username") or not request.form.get("password"):

            flash("Please type in a username and/or password!", "danger")

            return redirect("/login")

        # query database for user information
        content = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))

        # check if user exists
        if len(content) != 1:

            flash("Username is invalid", "danger")

            return redirect("/login")

        # check if password if correct
        elif not check_password_hash(content[0]["hash"], request.form.get("password")):

            flash("Password is invalid", "danger")

            return redirect("/login")

        else:

            # log user in
            session["user_id"] = content[0]["id"]

            # redirect user back to index
            return redirect("/")

    # user reached route via GET
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/")
@login_required
def index():

        # create dictionary and list
        List, Dict = [], {}

        #query table for dates
        plus = db.execute("SELECT * FROM plus WHERE user_id = :ID", ID = session["user_id"])

        # order elapsed time
        for i in range(len(plus)):

            # insert data into datetime function
            birthdate = datetime.datetime(datetime.date.today().year, int(plus[i]["month"]), int(plus[i]["day"]))

            elapsed = (birthdate - datetime.datetime.now()).days + 1

            if elapsed < 0:

                elapsed = elapsed + 365

            db.execute("UPDATE plus SET elapsed_time = :elapsed_time WHERE add_id = :add_id", elapsed_time=elapsed, add_id=plus[i]["add_id"])

        # get ordered data
        plus = db.execute("SELECT * FROM plus WHERE user_id = :ID ORDER BY elapsed_time ASC", ID=session["user_id"])

        for i in range(len(plus)):

            # insert data into datetime function
            birthdate = datetime.datetime(datetime.date.today().year, int(plus[i]["month"]), int(plus[i]["day"]))

            # insert into Dict
            Dict["elapsed_time"] = plus[i]["elapsed_time"]

            Dict["id"] = plus[i]["add_id"]

            Dict["name"] = plus[i]["name"]

            Dict["message"] = plus[i]["message"]

            Dict["year"] = plus[i]["year"]

            Dict["month"] = birthdate.strftime("%B")

            Dict["day"] = birthdate.strftime("%d")

            # insert into final list
            List.append({"id": Dict["id"], "name": Dict["name"], "message": Dict["message"], "year": Dict["year"], "month": Dict["month"], "day": Dict["day"], "elapsed_time": Dict["elapsed_time"]})

        return render_template("index.html", List=List, plus=len(plus))


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    # user reached route via POST
    if request.method == "POST":

        # get UserId
        ID = session["user_id"]

        # get month and day
        date = re.findall("\d+", str(request.form.get("birthdate")))

        # check for errors
        if not request.form.get("name") or not request.form.get("birthdate"):

            flash("Please fill in all of the required fields","danger")

            return redirect("/add")

        # insert id, name, month, and day into the database
        db.execute("INSERT INTO plus (user_id, name, month, day, year, message, elapsed_time) VALUES(?, ?, ?, ?, ?, ?, ?)", ID, request.form.get("name"), date[1], date[2], date[0], request.form.get("message"), 0)

        flash("Success!", "success")

        return redirect("/add")

    # user reached route via GET
    else:

        return render_template("add.html", datenow=datetime.date.today().year)


@app.route("/edit/<int:add_id>", methods=["GET", "POST"])
@login_required
def edit(add_id):

    if request.method == "GET":

        plus = db.execute("SELECT * FROM plus WHERE add_id = :ID", ID = add_id)

        return render_template("edit.html", name=plus[0]["name"], message=plus[0]["message"], add_id=add_id, delete=delete, datenow=datetime.date.today().year)

    # request method is POST
    else:

        plus = db.execute("SELECT * FROM plus WHERE add_id = :ID", ID = add_id)

        # find day, month, and year
        date = re.findall("\d+", str(request.form.get("birthdate")))

        print(date)

        # user filled birthdate
        if len(request.form.get("birthdate")) != 0:

            month = date[1]

            day = date[2]

            year = date[0]

        # user didnt fill in birthdate
        else:

            month = plus[0]["month"]

            day = plus[0]["day"]

            year = plus[0]["year"]

        # user filled in name
        if len(request.form.get("name")) != 0:

            name = request.form.get("name")

            message = request.form.get("message")

        # user didn't fill in name
        else:

            name = plus[0]["name"]

        # user filled in message
        if len(request.form.get("message")) != 0:

            message = request.form.get("message")

        # user didn't fill in message
        else:

            message = plus[0]["message"]

        print(f"this is cs50:{name}, {month}, {day}, {year}, {message}")

        # update information
        db.execute("UPDATE plus SET add_id = :add_id, user_id = :user_id, name = :name, month = :month, day = :day, year = :year, message = :message WHERE add_id = :add_id",
        add_id=add_id, user_id=session["user_id"], name=name,month=month,day=day,year=year,message=message)

        flash("Success!", "success")

        return redirect("/")

@app.route("/delete/<int:add_id>")
@login_required
def delete(add_id):

        #delete
        db.execute("DELETE FROM plus WHERE add_id = :ID", ID=add_id)

        flash("Deleted!","success")

        return redirect("/") 
        