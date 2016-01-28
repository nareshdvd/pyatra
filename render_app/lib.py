import subprocess
from subprocess import Popen
import os
import shutil
import requests

def process(args):
  pr = Popen(args, stderr=subprocess.STDOUT)
  pr.wait()

