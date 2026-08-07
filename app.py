import sys
import os

# Add the 'agent' folder to sys.path so nested modules (frontend, backend, config) resolve smoothly
agent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent")
if agent_dir not in sys.path:
    sys.path.insert(0, agent_dir)

# Import and execute the main Streamlit application
import app
