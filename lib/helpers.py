import subprocess
from subprocess import Popen
def run_process(args):
  pr = Popen(args, stderr=subprocess.STDOUT)
  pr.wait()