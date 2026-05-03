from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for tasks
todos = [{"id": 1, "task": "Sample Task", "completed": False}]

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Python To-Do Application</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f7f6; }
            .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            ul { list-style-type: none; padding: 0; }
            li { padding: 10px; background: #eee; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; border-radius: 4px; }
            .completed { text-decoration: line-through; color: gray; }
            form { display: flex; gap: 10px; margin-top: 20px; }
            input[type="text"] { flex-grow: 1; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
            button { padding: 8px 12px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
            .btn-danger { background: #dc3545; }
            .btn-warning { background: #ffc107; color: black; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Python To-Do List</h1>
            <ul>
                {% for todo in todos %}
                    <li>
                        <span class="{{ 'completed' if todo.completed else '' }}">{{ todo.task }}</span>
                        <div>
                            {% if not todo.completed %}
                                <a href="{{ url_for('complete', task_id=todo.id) }}"><button class="btn-warning">Complete</button></a>
                            {% endif %}
                            <a href="{{ url_for('delete', task_id=todo.id) }}"><button class="btn-danger">Delete</button></a>
                        </div>
                    </li>
                {% endfor %}
            </ul>
            <form action="/add" method="POST">
                <input type="text" name="task" placeholder="What needs to be done?" required>
                <button type="submit">Add</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task_text = request.form.get('task')
    new_id = max([t['id'] for t in todos], default=0) + 1
    todos.append({"id": new_id, "task": task_text, "completed": False})
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    global todos
    todos = [t for t in todos if t['id'] != task_id]
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    for todo in todos:
        if todo['id'] == task_id:
            todo['completed'] = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)