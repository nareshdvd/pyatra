import subprocess
from subprocess import Popen
import os
import shutil
import requests

def process(args):
  process_str = "__".join(args)
  print "INSIDE PROCESS {}".format(process_str)
  pr = Popen(args, stderr=subprocess.STDOUT)
  pr.wait()
  print "PROCESS  FINISHED {}".format(process_str)

