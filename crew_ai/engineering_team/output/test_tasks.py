```
import unittest
from datetime import datetime, timedelta
from typing import List, Dict, Union, Optional

class Task:
    def __init__(self, title: str, description: str, due_date: datetime, priority: int):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = False
        self.completion_date = None

    def mark_completed(self):
        self.completed = True
        self.completion_date = datetime.now()

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.completed_tasks_log: List[Dict[str, Union[str, datetime]] ] = []

    def add_task(self, title: str, description: str, due_date: datetime, priority: int) -> bool:
        if any(task.title == title and task.due_date == due_date for task in self.tasks):
            return False
        self.tasks.append(Task(title, description, due_date, priority))
        return True

    def delete_task(self, title: str, due_date: datetime) -> bool:
        for task in self.tasks:
            if task.title == title and task.due_date == due_date:
                self.tasks.remove(task)
                return True
        return False

    def mark_task_completed(self, title: str, due_date: datetime) -> bool:
        for task in self.tasks:
            if task.title == title and task.due_date == due_date:
                task.mark_completed()
                self.completed_tasks_log.append({"title": task.title, "completion_date": task.completion_date})
                return True
        return False

    def filter_tasks(self, completed: Optional[bool] = None, due_date: Optional[datetime] = None, 
                     priority: Optional[int] = None) -> List[Task]:
        filtered = self.tasks
        if completed is not None:
            filtered = [task for task in filtered if task.completed == completed]
        if due_date is not None:
            filtered = [task for task in filtered if task.due_date.date() == due_date.date()]
        if priority is not None:
            filtered = [task for task in filtered if task.priority == priority]
        return filtered

    def count_tasks(self) -> Dict[str, int]:
        count_pending = len([task for task in self.tasks if not task.completed])
        count_completed = len(self.completed_tasks_log)
        return {"pending": count_pending, "completed": count_completed}

    def upcoming_tasks(self) -> List[Task]:
        today = datetime.now()
        seven_days_later = today + timedelta(days=7)
        return [task for task in self.tasks if today <= task.due_date <= seven_days_later]

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.manager = TaskManager()

    def test_add_task_success(self):
        result = self.manager.add_task('Task 1', 'Description 1', datetime(2023, 12, 1), 2)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.tasks), 1)

    def test_add_task_duplicate(self):
        self.manager.add_task('Task 2', 'Description 2', datetime(2023, 12, 2), 3)
        result = self.manager.add_task('Task 2', 'Description 2', datetime(2023, 12, 2), 3)
        self.assertFalse(result)
        self.assertEqual(len(self.manager.tasks), 1)

    def test_delete_task_success(self):
        self.manager.add_task('Task 3', 'Description 3', datetime(2023, 12, 3), 4)
        result = self.manager.delete_task('Task 3', datetime(2023, 12, 3))
        self.assertTrue(result)
        self.assertEqual(len(self.manager.tasks), 0)

    def test_delete_task_not_found(self):
        result = self.manager.delete_task('Nonexistent Task', datetime(2023, 12, 3))
        self.assertFalse(result)

    def test_mark_task_completed_success(self):
        self.manager.add_task('Task 4', 'Description 4', datetime(2023, 12, 4), 1)
        result = self.manager.mark_task_completed('Task 4', datetime(2023, 12, 4))
        self.assertTrue(result)
        self.assertTrue(self.manager.tasks[0].completed)
        self.assertEqual(len(self.manager.completed_tasks_log), 1)

    def test_mark_task_completed_not_found(self):
        result = self.manager.mark_task_completed('Nonexistent Task', datetime(2023, 12, 4))
        self.assertFalse(result)

    def test_filter_tasks_by_completed(self):
        self.manager.add_task('Task 5', 'Description 5', datetime(2023, 12, 5), 5)
        self.manager.mark_task_completed('Task 5', datetime(2023, 12, 5))
        filtered = self.manager.filter_tasks(completed=True)
        self.assertEqual(len(filtered), 1)

    def test_filter_tasks_by_due_date(self):
        self.manager.add_task('Task 6', 'Description 6', datetime(2023, 12, 6), 2)
        filtered = self.manager.filter_tasks(due_date=datetime(2023, 12, 6))
        self.assertEqual(len(filtered), 1)

    def test_count_tasks(self):
        self.manager.add_task('Task 7', 'Description 7', datetime(2023, 12, 7), 2)
        self.manager.mark_task_completed('Task 7', datetime(2023, 12, 7))
        counts = self.manager.count_tasks()
        self.assertEqual(counts['pending'], 0)
        self.assertEqual(counts['completed'], 1)

    def test_upcoming_tasks(self):
        self.manager.add_task('Task 8', 'Description 8', datetime.now() + timedelta(days=5), 1)
        upcoming = self.manager.upcoming_tasks()
        self.assertEqual(len(upcoming), 1) 
        
if __name__ == '__main__':
    unittest.main()
```