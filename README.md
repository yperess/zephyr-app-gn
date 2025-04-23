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

Regenerate cmake build
```
rm -fr build_cmake/ ; ZEPHYR_SDK_INSTALL_DIR=$(pwd)/toolchain Zephyr_DIR=$(pwd)/zephyr cmake -Bbuild_cmake -GNinja -DZEPHYR_MODULES="$(pwd)/modules/hal/atmel;$(pwd)/modules/hal/cmsis" -DBOARD=robokit1 -DZEPHYR_SDK_INSTALL_DIR=$(pwd)/toolchain app/ ; ninja -Cbuild_cmake libzephyr.a -v -j 1 | tee build_cmake/build.log
```

Regenerate gn build
```
rm -fr out ; gn gen out ; ninja -Cout build_zephyr_lib | tee out/build.log
```