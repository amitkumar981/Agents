#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from financial_researcher.crew import FinancialResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        "company": "Tesla",
        "current_year": datetime.now().year
    }
    
    result = FinancialResearcher().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    try:
        print(result.raw)
    except AttributeError:
        print(result.output)

    print("\n\nReport has been saved to output/report.md")


if __name__ == "__main__":
    run()




