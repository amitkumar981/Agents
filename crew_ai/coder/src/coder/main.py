#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from coder.crew import Coder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# New assignment description
assignment = (
    "Write a Python program that generates the Fibonacci sequence up to "
    "the 50th term and saves the sequence to a text file named 'fibonacci.txt'."
)

def run():
    """
    Run the crew with the assignment
    """
    inputs = {
        "assignment": assignment
    }
    result = Coder().crew().kickoff(inputs=inputs)
    
    # Handle result safely depending on CrewAI version
    print(getattr(result, "output", result))
