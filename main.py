import subprocess
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

subprocess.Popen(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cbot1.py'))
subprocess.Popen(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cbot2.py'))