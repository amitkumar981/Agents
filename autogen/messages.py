from dataclasses import dataclass
from autogen_core import AgentId
import glob
import os
import random

@dataclass
class Message:
    content: str

def find_recipient() -> AgentId:
    try:
        # find all python files starting with "agent"
        agent_files = glob.glob("agent*.py")

        # extract names without extension
        agent_names = [os.path.splitext(os.path.basename(file))[0] for file in agent_files]

        # remove base "agent" file if exists
        if "agent" in agent_names:
            agent_names.remove("agent")

        # choose random agent
        agent_name = random.choice(agent_names)
        print(f"Selecting agent for refinement: {agent_name}")
        return AgentId(agent_name, "default")

    except Exception as e:
        print(f"Exception finding recipient: {e}")
        return AgentId("agent1", "default")
