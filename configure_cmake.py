import subprocess
import sys
import os 

def main():
  # Set the environment variable to point to where zephyr lives
  dir_path = os.path.dirname(os.path.realpath(__file__))
  os.environ['Zephyr_DIR'] = dir_path + "/zephyr"

  #Application
  app = dir_path + "/app/"

  # Run CMake
  subprocess.run(['cmake', '-Bbuild_cmake', '-GNinja', '-DBOARD=robokit1', app])

if __name__ == '__main__':
  sys.exit(main());
