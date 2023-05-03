from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config.from_object("config")


class Todo:
    def __init__(self, title, done=False):
        self.title = title
        self.done = done


todo_list = []


@app.route("/")
def index():
    global todo_list
    return render_template("index.html", todos=todo_list)


@app.route("/add", methods=["POST"])
def add():
    global todo_list
    todo_title = request.form["title"]
    todo = Todo(todo_title, False)
    todo_list.append(todo)
    return redirect("/")


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    global todo_list
    todo_list.pop(todo_id)
    return redirect("/")


@app.route("/update/<int:todo_id>")
def update(todo_id):
    global todo_list
    todo = todo_list[todo_id]
    if todo.done:
        todo.done = False
    else:
        todo.done = True
    return redirect("/")


if __name__ == "__main__":
    app.run()
