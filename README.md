# GN build experiment
```bash
$ git clone ...
$ cd ...
$ python3 -m venv .venv
$ source .venv/bin/activate
```

## Starting off with West

Download all the dependencies
```bash
$ pip install west
$ west init -l manifest
$ west update
```

Install the Python dependencies
```bash
$ pip install -r zephyr/scripts/requirements.txt
```

Build the app:
```bash
$ west build -p -b robokit1 app
```

## Building manually with CMake
Remove West:
```bash
$ pip uninstall west
```

Configure the project:
```bash
$ Zephyr_DIR=$(pwd)/zephyr cmake -Bbuild_cmake -GNinja \
-DZEPHYR_MODULES="$(pwd)/modules/hal/atmel;$(pwd)/modules/hal/cmsis" \
-DBOARD=robokit1 \
app/
```

Build the app:
```bash
$ ninja -Cbuild_cmake
```

Build libzephyr.a:
```bash
$ ninja -Cbuild_cmake libzephyr.a
```
