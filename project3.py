import tkinter as tk
from tkinter import messagebox
import datetime

class DayPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Day Planner (Reminder)")
        self.root.geometry("600x600")

        # Dictionary to store tasks with datetime as keys
        self.tasks = {}

        # Input fields for task description, date, and time
        self.task_desc_label = tk.Label(root, text="Task Description:")
        self.task_desc_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.task_desc_entry = tk.Entry(root, width=30)
        self.task_desc_entry.grid(row=0, column=1, pady=5, padx=5)

        self.task_date_label = tk.Label(root, text="Task Date (YYYY-MM-DD):")
        self.task_date_label.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        self.task_date_entry = tk.Entry(root, width=30)
        self.task_date_entry.grid(row=1, column=1, pady=5, padx=5)

        self.task_time_label = tk.Label(root, text="Task Time (HH:MM):")
        self.task_time_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.task_time_entry = tk.Entry(root, width=30)
        self.task_time_entry.grid(row=2, column=1, pady=5, padx=5)

        # Add Task button with color
        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task, bg="#5bc0de", fg="black", width=15)
        self.add_task_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Labels for task categories
        self.incomplete_tasks_label = tk.Label(root, text="Incomplete Tasks:", font=("Helvetica", 10, "bold"))
        self.incomplete_tasks_label.grid(row=4, column=0, pady=5, sticky="w")

        self.completed_tasks_label = tk.Label(root, text="Completed Tasks:", font=("Helvetica", 10, "bold"))
        self.completed_tasks_label.grid(row=6, column=0, pady=5, sticky="w")

        self.failed_tasks_label = tk.Label(root, text="Failed Tasks:", font=("Helvetica", 10, "bold"))
        self.failed_tasks_label.grid(row=8, column=0, pady=5, sticky="w")

        # Frames and Listboxes for tasks
        self.incomplete_task_frame = tk.Frame(root)
        self.incomplete_task_frame.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

        self.completed_task_listbox = tk.Listbox(root, width=50, height=5)
        self.completed_task_listbox.grid(row=7, column=0, columnspan=2, pady=5)

        self.failed_task_listbox = tk.Listbox(root, width=50, height=5)
        self.failed_task_listbox.grid(row=9, column=0, columnspan=2, pady=5)

        # To keep track of task updates for countdown
        self.update_task_countdown()

    def add_task(self):
        task_name = self.task_desc_entry.get()
        task_date = self.task_date_entry.get()
        task_time = self.task_time_entry.get()

        try:
            task_datetime = datetime.datetime.strptime(f"{task_date} {task_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Invalid Input", "Invalid date or time format. Please try again.")
            return

        if task_datetime < datetime.datetime.now():
            messagebox.showerror("Invalid Task Time", "Cannot add a task with a past date/time.")
            return

        self.tasks[task_datetime] = {'task': task_name, 'completed': False, 'failed': False, 'reminder_shown': False}
        self.task_desc_entry.delete(0, tk.END)
        self.task_date_entry.delete(0, tk.END)
        self.task_time_entry.delete(0, tk.END)
        self.show_tasks()

    def mark_task_completed(self, task_datetime):
        self.tasks[task_datetime]['completed'] = True
        messagebox.showinfo("Task Completed", f"Task '{self.tasks[task_datetime]['task']}' marked as completed.")
        self.show_tasks()

    def delete_task(self, task_datetime):
        del self.tasks[task_datetime]
        messagebox.showinfo("Task Deleted", "The task has been deleted.")
        self.show_tasks()

    def show_tasks(self):
        # Clear the incomplete task frame, completed task listbox, and failed task listbox
        for widget in self.incomplete_task_frame.winfo_children():
            widget.destroy()
        self.completed_task_listbox.delete(0, tk.END)
        self.failed_task_listbox.delete(0, tk.END)

        now = datetime.datetime.now()

        # Display incomplete tasks with buttons
        for task_datetime, details in sorted(self.tasks.items()):
            if not details['completed'] and not details['failed']:
                task_info = f"{details['task']} at {task_datetime} (Time left: {self.time_left(task_datetime)})"

                task_row = tk.Frame(self.incomplete_task_frame)
                task_row.pack(fill="x", pady=2)

                task_label = tk.Label(task_row, text=task_info, anchor="w", width=50)
                task_label.pack(side="left", padx=5)

                complete_button = tk.Button(task_row, text="Complete", bg="#92c87c", fg="white",
                                            command=lambda dt=task_datetime: self.mark_task_completed(dt))
                complete_button.pack(side="left", padx=5)

                delete_button = tk.Button(task_row, text="Delete", bg="#f15c5c", fg="white",
                                          command=lambda dt=task_datetime: self.delete_task(dt))
                delete_button.pack(side="left", padx=5)

        # Display completed tasks
        for task_datetime, details in sorted(self.tasks.items()):
            if details['completed']:
                task_info = f"{details['task']} at {task_datetime} (Completed)"
                self.completed_task_listbox.insert(tk.END, task_info)

        # Display failed tasks
        for task_datetime, details in sorted(self.tasks.items()):
            if details['failed']:
                task_info = f"{details['task']} at {task_datetime} (Failed)"
                self.failed_task_listbox.insert(tk.END, task_info)

    def time_left(self, task_datetime):
        now = datetime.datetime.now()
        if task_datetime > now:
            time_diff = task_datetime - now
            return str(time_diff).split('.')[0]  # Return time in hours:minutes:seconds
        else:
            return "Task already passed"

    def update_task_countdown(self):
        now = datetime.datetime.now()
        for task_datetime, details in self.tasks.items():
            if not details['completed'] and not details['failed']:
                time_diff = (task_datetime - now).total_seconds()

                if 0 < time_diff <= 1800 and not details['reminder_shown']:  # 30 minutes = 1800 seconds
                    messagebox.showinfo("Reminder", f"Task '{details['task']}' has 30 minutes or less remaining!")
                    details['reminder_shown'] = True

                if time_diff <= 0:
                    details['failed'] = True

        self.show_tasks()
        self.root.after(1000, self.update_task_countdown)  # Update every second


def main():
    root = tk.Tk()
    planner = DayPlanner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
