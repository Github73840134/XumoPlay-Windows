import os, sys
os.chdir(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(os.path.dirname(os.getcwd()), "libs"))
import subprocess
subprocess.run(f"../core/python.exe XumoPlayApp.py {' '.join(sys.argv[1:])}")