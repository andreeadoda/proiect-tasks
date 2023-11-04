import tkinter as tk
import sqlite3
from datetime import datetime, timedelta
from tkinter import messagebox

# Conectarea la baza de date SQLite
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, deadline DATE)''')
conn.commit()

def add_task():
    task = task_entry.get()
    deadline = deadline_entry.get()
    try:
        cursor.execute("INSERT INTO tasks (task, deadline) VALUES (?, ?)", (task, deadline))
        conn.commit()
        task_entry.delete(0, tk.END)
        deadline_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Eroare", "Eroare la adăugarea task-ului: " + str(e))

def show_tasks():
    task_list.delete(0, tk.END)
    for row in cursor.execute("SELECT task, deadline FROM tasks"):
        task, deadline = row
        task_list.insert(tk.END, f'Task: {task}, Deadline: {deadline}')

def check_deadlines():
    today = datetime.now().date()
    for row in cursor.execute("SELECT task, deadline FROM tasks"):
        task, deadline = row
        if today == datetime.strptime(deadline, "%Y-%m-%d").date():
            messagebox.showwarning("Notificare", f"Task-ul '{task}' are termenul limită astăzi!")

# Crearea ferestrei principale
root = tk.Tk()
root.title("Task Scheduler")
root.configure(bg="pink")



# Etichete și câmpuri
task_label = tk.Label(root, text="Task:",fg="blue")
task_label.pack()
task_entry = tk.Entry(root)
task_entry.pack()

deadline_label = tk.Label(root, text="Deadline (YYYY-MM-DD):")
deadline_label.pack()
deadline_entry = tk.Entry(root)
deadline_entry.pack()

# Buton pentru adăugarea task-urilor
add_button = tk.Button(root, text="Adăugare Task", command=add_task)
add_button.pack()

task_list = tk.Listbox(root)
task_list.pack()

show_button = tk.Button(root, text="Afișare Task-uri", command=show_tasks,bg="blue")
show_button.pack()

# Buton pentru verificarea deadline-urilor
check_button = tk.Button(root, text="Verificare Termen Limită", command=check_deadlines)
check_button.pack()


check_deadlines()

root.mainloop()


conn.close()
