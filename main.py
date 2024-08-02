import subprocess
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

subprocess.Popen('cbot1.py')
subprocess.Popen('cbot2.py')