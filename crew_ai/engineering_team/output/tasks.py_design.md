```python
# tasks.py

from datetime import datetime, timedelta
from typing import List, Dict, Union, Optional

class Task:
    def __init__(self, title: str, description: str, due_date: datetime, priority: int):
        """
        Initializes a task with title, description, due date, and priority level.
        
        :param title: Title of the task.
        :param description: Description of the task.
        :param due_date: Due date of the task as a datetime object.
        :param priority: Priority level of the task (1 to 5, where 1 is highest priority).
        """
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = False
        self.completion_date = None

    def mark_completed(self):
        """
        Marks the task as completed and records the completion date.
        """
        self.completed = True
        self.completion_date = datetime.now()

class TaskManager:
    def __init__(self):
        """
        Initializes the Task Manager with an empty task list and completed task log.
        """
        self.tasks: List[Task] = []
        self.completed_tasks_log: List[Dict[str, Union[str, datetime]] ] = []

    def add_task(self, title: str, description: str, due_date: datetime, priority: int) -> bool:
        """
        Adds a new task if it does not already exist with the same title and due date.

        :param title: Title of the task.
        :param description: Description of the task.
        :param due_date: Due date of the task as a datetime object.
        :param priority: Priority level of the task (1 to 5).
        :return: True if task was added, False if a duplicate task exists.
        """
        if any(task.title == title and task.due_date == due_date for task in self.tasks):
            return False  # Duplicate task found
        self.tasks.append(Task(title, description, due_date, priority))
        return True

    def delete_task(self, title: str, due_date: datetime) -> bool:
        """
        Deletes a task by title and due date.

        :param title: Title of the task.
        :param due_date: Due date of the task as a datetime object.
        :return: True if task was deleted, False if not found.
        """
        for task in self.tasks:
            if task.title == title and task.due_date == due_date:
                self.tasks.remove(task)
                return True
        return False

    def mark_task_completed(self, title: str, due_date: datetime) -> bool:
        """
        Marks a task as completed and logs its completion.

        :param title: Title of the task.
        :param due_date: Due date of the task as a datetime object.
        :return: True if task was marked completed, False if not found.
        """
        for task in self.tasks:
            if task.title == title and task.due_date == due_date:
                task.mark_completed()
                self.completed_tasks_log.append({
                    "title": task.title,
                    "completion_date": task.completion_date
                })
                return True
        return False

    def filter_tasks(self, completed: Optional[bool] = None, due_date: Optional[datetime] = None, 
                     priority: Optional[int] = None) -> List[Task]:
        """
        Filters tasks based on provided criteria.

        :param completed: Completion status to filter tasks.
        :param due_date: Due date to filter tasks.
        :param priority: Priority level to filter tasks.
        :return: List of filtered tasks.
        """
        filtered = self.tasks
        if completed is not None:
            filtered = [task for task in filtered if task.completed == completed]
        if due_date is not None:
            filtered = [task for task in filtered if task.due_date.date() == due_date.date()]
        if priority is not None:
            filtered = [task for task in filtered if task.priority == priority]
        return filtered

    def count_tasks(self) -> Dict[str, int]:
        """
        Counts the number of pending and completed tasks.

        :return: Dictionary with counts of pending and completed tasks.
        """
        count_pending = len([task for task in self.tasks if not task.completed])
        count_completed = len(self.completed_tasks_log)
        return {
            "pending": count_pending,
            "completed": count_completed
        }

    def upcoming_tasks(self) -> List[Task]:
        """
        Returns a list of tasks due within the next 7 days.

        :return: List of upcoming tasks.
        """
        today = datetime.now()
        seven_days_later = today + timedelta(days=7)
        return [task for task in self.tasks if today <= task.due_date <= seven_days_later]
```

### Explanation of Functions and Methods

1. **Task Class**
   - `__init__`: Initializes the task attributes.
   - `mark_completed`: Marks the task as completed and records the completion timestamp.

2. **TaskManager Class**
   - `__init__`: Initializes empty task list and completed task log.
   - `add_task`: Adds a task if it does not exist already (title and due date uniqueness).
   - `delete_task`: Deletes a specific task identified by title and due date.
   - `mark_task_completed`: Marks a specified task as completed and logs the completion.
   - `filter_tasks`: Filters tasks based on completion status, due date, and priority.
   - `count_tasks`: Returns a count of pending and completed tasks.
   - `upcoming_tasks`: Returns tasks that are due in the next 7 days.
  
This design provides a comprehensive task management system that adheres to the requirements stated, is easy to integrate into a UI, and is straightforward to test.