from flask import Flask, render_template, request, redirect
from wtforms import Form, StringField, SubmitField
from wtforms.validators import InputRequired
from models import db, Todo

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config.from_pyfile("config.py")

db.init_app(app)


class TodoForm(Form):
    title = StringField("What needs to be done?", [InputRequired()])
    submit = SubmitField("Add")


@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos, form=TodoForm())


@app.route("/add", methods=["POST"])
def add():
    form = TodoForm(request.form)
    if request.method == "POST" and form.validate():
        todo = Todo(title=request.form["title"], complete=False)
        db.session.add(todo)
        db.session.commit()
    return redirect("/")


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    if request.method == "POST":
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")


@app.route("/update/<int:todo_id>", methods=["POST"])
def update(todo_id):
    if request.method == "POST":
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
