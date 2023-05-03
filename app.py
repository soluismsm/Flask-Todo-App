from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object("config")

db.init_app(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    todo = Todo(title=request.form["title"], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect("/")


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.complete:
        todo.complete = False
    else:
        todo.complete = True
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
