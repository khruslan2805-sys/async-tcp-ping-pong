import subprocess
import time
import sys

PYTHON = sys.executable

server = subprocess.Popen([PYTHON, "server.py"])
client1 = subprocess.Popen([PYTHON, "client.py", "1"])
client2 = subprocess.Popen([PYTHON, "client.py", "2"])

print("Running system for 5 minutes...")

time.sleep(300)

server.terminate()
client1.terminate()
client2.terminate()

print("Stopped.")

