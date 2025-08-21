import sys
import warnings
import os
from datetime import datetime

from engineering_team.crew import engineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

requirements = """
A simple task management system for a personal productivity app.
The system should allow users to create tasks with a title, description, due date, and priority level.
The system should allow users to mark tasks as completed or delete them.
The system should support filtering tasks by completion status, due date, and priority.
The system should calculate and report the number of pending tasks and completed tasks.
The system should provide a summary of upcoming tasks that are due within the next 7 days.
The system should maintain a log of all completed tasks with their completion date.
The system should prevent creating duplicate tasks with the same title and due date.
"""

module_name = "tasks.py"
class_name = "TaskManager"


def run():
    """
    Run the research crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }

    # Create and run the crew
    result = engineeringTeam().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
