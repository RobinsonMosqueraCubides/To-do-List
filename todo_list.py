import tkinter as tk
from tkinter import messagebox
import sqlite3

# Funciones de la base de datos
def connect_db():
    return sqlite3.connect('todo_list.db')

def create_task(task):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, done) VALUES (?, 0)", (task,))
    conn.commit()
    conn.close()

def fetch_tasks():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT id, task, done FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

def update_task(task_id, done):
    conn = connect_db()
    c = conn.cursor()
    c.execute("UPDATE tasks SET done = ? WHERE id = ?", (done, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Funciones de la interfaz gráfica
def add_task():
    task = entry.get()
    if task:
        create_task(task)
        entry.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showwarning("Advertencia", "El campo de tarea está vacío")

def toggle_task(task_id, done):
    new_done = not done
    update_task(task_id, new_done)
    load_tasks()

def remove_task(task_id):
    delete_task(task_id)
    load_tasks()

def load_tasks():
    for widget in frame.winfo_children():
        widget.destroy()

    tasks = fetch_tasks()
    for task_id, task, done in tasks:
        checkbox = tk.Checkbutton(frame, text=task, variable=tk.BooleanVar(value=done),
                                 command=lambda t_id=task_id, t_done=done: toggle_task(t_id, t_done))
        checkbox.pack(anchor="w")
        delete_button = tk.Button(frame, text="Eliminar", command=lambda t_id=task_id: remove_task(t_id))
        delete_button.pack(anchor="e")

# Configuración de la ventana principal
root = tk.Tk()
root.title("To-Do List")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

add_button = tk.Button(root, text="Agregar Tarea", command=add_task)
add_button.pack()

load_tasks()

root.mainloop()
