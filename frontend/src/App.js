import { useEffect, useState } from "react";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  const API_URL = "http://localhost:5000/tasks";

  useEffect(() => {
    fetch(API_URL)
      .then((response) => response.json())
      .then((data) => setTasks(data))
      .catch((error) => console.error("Error fetching tasks:", error));
  }, []);

  const addTask = () => {
    fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title }),
    })
      .then((response) => response.json())
      .then((newTask) => {
        setTasks([...tasks, newTask]);
        setTitle("");
      })
      .catch((error) => console.error("Error adding task:", error));
  };

  const toggleDone = (task) => {
    fetch(`${API_URL}/${task.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ completed: !task.completed }),
    })
      .then((response) => response.json())
      .then((updatedTask) => {
        setTasks(tasks.map((t) => (t.id === updatedTask.id ? updatedTask : t)));
      })
      .catch((error) => console.error("Error updating task:", error));
  };

  const deleteTask = (id) => {
    fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    })
      .then(() => {
        setTasks(tasks.filter((t) => t.id !== id));
      })
      .catch((error) => console.error("Error deleting task:", error));
  };

  return (
    <div style={{ padding: 20 }} className="App">
      <h2>Task Manager</h2>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter task title"
      />
      <button onClick={addTask}>Add Task</button>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <span
              style={{
                textDecoration: task.completed ? "line-through" : "none",
                marginRight: 10,
              }}
            >
              {task.title}
            </span>
            <button onClick={() => toggleDone(task)}>
              {task.completed ? "Undo" : "Mark Done"}
            </button>
            <button
              onClick={() => deleteTask(task.id)}
              style={{ marginLeft: 5 }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
