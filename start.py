import subprocess

subprocess.Popen(["python", "main.py"])
subprocess.Popen(["python", "agent.py"])
subprocess.Popen(["python", "auto_loop.py"])

# Keep it alive
while True:
    pass