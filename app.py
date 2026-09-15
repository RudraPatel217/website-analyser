import sys
import os

# Add the 'agent' folder to sys.path so nested modules (frontend, backend, config) resolve smoothly
agent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent")
if agent_dir not in sys.path:
    sys.path.insert(0, agent_dir)

# Execute agent/app.py directly in the runner script namespace on every run and rerun
agent_app_path = os.path.join(agent_dir, "app.py")
with open(agent_app_path, "r", encoding="utf-8") as _f:
    _code = compile(_f.read(), agent_app_path, "exec")
exec(_code, globals())
