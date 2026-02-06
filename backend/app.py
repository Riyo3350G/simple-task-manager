from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route("/")
def home():
    return {"message": "Backend is running!"}


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify(
        [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]
    )


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title or not str(title).strip():
        return jsonify({"error": "title is required"}), 400

    new_task = Task(title=title.strip())
    db.session.add(new_task)
    db.session.commit()

    return (
        jsonify(
            {
                "id": new_task.id,
                "title": new_task.title,
                "completed": new_task.completed,
            }
        ),
        201,
    )


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json(silent=True) or {}

    task.title = data.get("title", task.title)
    task.completed = data.get("completed", task.completed)

    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "completed": task.completed})


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
