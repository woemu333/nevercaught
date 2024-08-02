import subprocess
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

subprocess.Popen('python cbot1.py')
subprocess.Popen('python cbot2.py')