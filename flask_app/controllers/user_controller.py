from flask import render_template, redirect, session, request
from flask_bcrypt import Bcrypt


from flask_app import app
from flask_app.models.user import User


bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/register", methods = ["POST"])
def register_user():

    if not User.register_validator(request.form):
        return redirect("/")

    hashing = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        "password": hashing
    }

    user_id = User.create(data)
    session["uuid"] = user_id
    print(user_id)
    
    return redirect("/user/account")


@app.route("/login", methods = ["POST"])
def login():
    if not User.login_validator(request.form):
        return redirect("/")

    user = User.get_by_email({"email": request.form["email"]})
    
    session["uuid"] = user.id

    return redirect("/user/account")


@app.route("/user/logout")
def logout():
    session.clear
    return redirect("/")



@app.route("/user/account")
def account_page():
    return render_template("account.html", user = User.get_by_id({"id": session['uuid']}))


@app.route("/user/<id>/edit")
def edit(id):
    return render_template("edit_user.html", user = User.get_one({"id": id}))


@app.route("/user/<id>/update", methods = ["POST"])
def update_user(id):
    print(request.form)
    data = {
        **request.form,
        "id": id
    }
    User.update(data)
    return redirect(f"/user/{id}")


@app.route("/user/<id>")
def display_user(id):
    return render_template("user_page.html", user = User.get_one({"id": id}))

@app.route("/user/<id>/delete")
def delete(id):
    User.delete({"id": id})
    return redirect("/")
