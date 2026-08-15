import os
import sys
import shutil
import subprocess
import time
import requests

def get_screenshot_service_dir():
    """
    Locates the 'screenshot-service' directory relative to the project root.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__)) # agent/backend
    project_root = os.path.abspath(os.path.join(current_dir, "..", "..")) # project root
    service_dir = os.path.join(project_root, "screenshot-service")
    return service_dir

def check_service_health(port=3000, timeout=1.5):
    """
    Checks if the local Puppeteer Express screenshot service is active on port 3000.
    """
    try:
        resp = requests.get(f"http://localhost:{port}/health", timeout=timeout)
        if resp.status_code == 200:
            data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
            return True, "Service running"
    except Exception as e:
        return False, str(e)
    return False, "Health check failed"

def is_node_installed():
    """
    Verifies if Node.js and npm are available on the user's host machine.
    """
    node_path = shutil.which("node") or shutil.which("node.exe")
    npm_path = shutil.which("npm") or shutil.which("npm.cmd")
    return bool(node_path and npm_path)

def install_and_start_puppeteer_service(progress_callback=None):
    """
    Automates dependency installation (npm install) and background server startup for Puppeteer.
    Returns (success: bool, message: str).
    """
    # 1. Check health first to avoid duplicate launch
    is_healthy, _ = check_service_health()
    if is_healthy:
        return True, "Puppeteer service is already running on port 3000."

    # 2. Check Node.js prerequisite
    if not is_node_installed():
        return False, "Node.js and npm were not found on your system PATH. Please install Node.js (v16+) from https://nodejs.org/ to use local browser previews."

    service_dir = get_screenshot_service_dir()
    if not os.path.exists(service_dir):
        return False, f"Screenshot service directory not found at path: {service_dir}"

    node_modules_dir = os.path.join(service_dir, "node_modules")

    # 3. Run 'npm install' if dependencies are missing
    if not os.path.exists(node_modules_dir):
        if progress_callback:
            progress_callback("Installing Puppeteer and Express Node.js dependencies (this may take a minute on first run)...")
        
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        try:
            install_proc = subprocess.run(
                [npm_cmd, "install"],
                cwd=service_dir,
                capture_output=True,
                text=True,
                shell=(sys.platform == "win32")
            )
            if install_proc.returncode != 0:
                return False, f"npm install failed: {install_proc.stderr[:300]}"
        except Exception as e:
            return False, f"Failed to execute npm install: {str(e)}"

    # 4. Launch 'node server.js' as a background process
    if progress_callback:
        progress_callback("Starting Puppeteer Express screenshot service on port 3000...")

    node_bin = shutil.which("node") or shutil.which("node.exe") or "node"
    server_script = os.path.join(service_dir, "server.js")

    try:
        if sys.platform == "win32":
            subprocess.Popen(
                [node_bin, server_script],
                cwd=service_dir,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            subprocess.Popen(
                [node_bin, server_script],
                cwd=service_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp
            )
    except Exception as e:
        return False, f"Failed to start node server.js: {str(e)}"

    # 5. Poll health endpoint for up to 20 seconds until online
    for attempt in range(20):
        time.sleep(1)
        healthy, _ = check_service_health()
        if healthy:
            return True, "Puppeteer service successfully installed and started on port 3000!"

    return False, "Started Puppeteer service process, but health check timed out on port 3000. Please check if port 3000 is blocked or occupied by another application."

