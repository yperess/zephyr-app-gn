import subprocess
import sys
import os 

def main():
  subprocess.run(['ninja', '-Cbuild_cmake', 'libzephyr.a'])

if __name__ == '__main__':
  sys.exit(main());

