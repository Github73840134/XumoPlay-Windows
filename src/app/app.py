import os, sys

os.chdir(os.path.dirname(__file__))
sys.path.insert(0,os.path.join(os.path.dirname(os.getcwd()), "libs"))
import subprocess
if "wait" in sys.argv:
	subprocess.run(f"../core/pythonw.exe XumoPlayApp.py {' '.join(sys.argv[1:])}")
else:
	subprocess.Popen(f"../core/pythonw.exe XumoPlayApp.py {' '.join(sys.argv[1:])}")
