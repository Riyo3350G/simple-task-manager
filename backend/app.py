from flask import Flask, jsonify, request

app = Flask(__name__)


tasks = []
task_id = 1


@app.route("/")
def home():
    return {"message": "Backend is running!"}


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id
    data = request.get_json()
    task = {"id": task_id, "title": data.get("title"), "completed": False}
    tasks.append(task)
    task_id += 1
    return task, 201


if __name__ == "__main__":
    app.run(debug=True)
