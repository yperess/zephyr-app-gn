import subprocess
import sys
import os 

def main():
  # Set the environment variable to point to where zephyr lives
  dir_path = os.path.dirname(os.path.realpath(__file__))
  os.environ['Zephyr_DIR'] = dir_path + "/zephyr"

  # Setup modules
  modules = "-DZEPHYR_MODULES="+dir_path+"/modules/hal/atmel;"+dir_path+"/modules/hal/cmsis"

  #Application
  app = dir_path + "/app/"

  # Run CMake
  subprocess.run(['cmake', '-Bbuild_cmake', '-GNinja', modules, '-DBOARD=robokit1', app])

if __name__ == '__main__':
  sys.exit(main());
