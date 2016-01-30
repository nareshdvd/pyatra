import subprocess
from subprocess import Popen
import os
import shutil
import requests

def process(args):
  print "INSIDE PROCESS"
  pr = Popen(args, stderr=subprocess.STDOUT)
  pr.wait()

