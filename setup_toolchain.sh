#!/bin/bash
cd toolchain
wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.17.0/toolchain_linux-x86_64_arm-zephyr-eabi.tar.xz
tar xvf toolchain_linux-x86_64_arm-zephyr-eabi.tar.xz
rm toolchain_linux-x86_64_arm-zephyr-eabi.tar.xz