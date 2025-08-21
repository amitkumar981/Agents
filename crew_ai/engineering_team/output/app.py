import gradio as gr
from datetime import datetime
from typing import Optional
from tasks import TaskManager

task_manager = TaskManager()

def add_task(title: str, description: str, due_date: str, priority: int):
    try:
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
        success = task_manager.add_task(title, description, due_date_obj, priority)
        return "Task added successfully!" if success else "Task already exists!"
    except ValueError:
        return "Invalid due date format. Please use YYYY-MM-DD."

def delete_task(title: str, due_date: str):
    try:
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
        success = task_manager.delete_task(title, due_date_obj)
        return "Task deleted successfully!" if success else "Task not found!"
    except ValueError:
        return "Invalid due date format. Please use YYYY-MM-DD."

def mark_completed(title: str, due_date: str):
    try:
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
        success = task_manager.mark_task_completed(title, due_date_obj)
        return "Task marked as completed!" if success else "Task not found!"
    except ValueError:
        return "Invalid due date format. Please use YYYY-MM-DD."

def filter_tasks(completed: bool, due_date: str = "", priority: Optional[int] = None):
    try:
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
    except ValueError:
        return [["Invalid date format. Use YYYY-MM-DD.", "", "", ""]]
    
    tasks = task_manager.filter_tasks(completed, due_date_obj, priority if priority and priority > 0 else None)
    return [(task.title, task.description, task.due_date.strftime("%Y-%m-%d"), task.priority) for task in tasks]

def task_count():
    counts = task_manager.count_tasks()
    return f"Pending tasks: {counts['pending']}, Completed tasks: {counts['completed']}"

def upcoming_tasks_summary():
    tasks = task_manager.upcoming_tasks()
    return [(task.title, task.due_date.strftime("%Y-%m-%d")) for task in tasks]

with gr.Blocks() as app:
    gr.Markdown("## ✅ Simple Task Management System")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### ➕ Add Task")
            title_input = gr.Textbox(label="Task Title")
            description_input = gr.Textbox(label="Description", lines=2)
            due_date_input = gr.Textbox(label="Due Date (YYYY-MM-DD)")
            priority_input = gr.Slider(label="Priority", minimum=1, maximum=5, step=1)
            add_button = gr.Button("Add Task")
            add_output = gr.Textbox(label="Add Task Result", interactive=False)
            add_button.click(add_task, inputs=[title_input, description_input, due_date_input, priority_input], outputs=add_output)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🗑️ Delete Task")
            delete_title_input = gr.Textbox(label="Task Title")
            delete_due_date_input = gr.Textbox(label="Due Date (YYYY-MM-DD)")
            delete_button = gr.Button("Delete Task")
            delete_output = gr.Textbox(label="Delete Task Result", interactive=False)
            delete_button.click(delete_task, inputs=[delete_title_input, delete_due_date_input], outputs=delete_output)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### ✅ Mark Task Completed")
            complete_title_input = gr.Textbox(label="Task Title")
            complete_due_date_input = gr.Textbox(label="Due Date (YYYY-MM-DD)")
            complete_button = gr.Button("Complete Task")
            complete_output = gr.Textbox(label="Complete Task Result", interactive=False)
            complete_button.click(mark_completed, inputs=[complete_title_input, complete_due_date_input], outputs=complete_output)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🔍 Filter Tasks")
            completed_input = gr.Checkbox(label="Show Completed Tasks", value=False)
            filter_due_date_input = gr.Textbox(label="Due Date (YYYY-MM-DD)")
            filter_priority_input = gr.Slider(label="Priority (Leave as 0 to ignore)", minimum=0, maximum=5, step=1, value=0)
            filter_button = gr.Button("Filter Tasks")
            filter_output = gr.Dataframe(headers=["Title", "Description", "Due Date", "Priority"], label="Filtered Tasks")
            filter_button.click(filter_tasks, inputs=[completed_input, filter_due_date_input, filter_priority_input], outputs=filter_output)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📊 Task Count")
            count_button = gr.Button("Count Tasks")
            count_output = gr.Textbox(label="Task Count", interactive=False)
            count_button.click(task_count, outputs=count_output)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### ⏳ Upcoming Tasks (Next 7 Days)")
            upcoming_button = gr.Button("Show Upcoming Tasks")
            upcoming_output = gr.Dataframe(headers=["Title", "Due Date"], label="Upcoming Tasks")
            upcoming_button.click(upcoming_tasks_summary, outputs=upcoming_output)

app.launch()
