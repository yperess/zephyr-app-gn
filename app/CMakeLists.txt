cmake_minimum_required(VERSION 3.13.1)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

project(app LANGUAGES C CXX)

if(DEFINED HEARABLES_APP_LIB)
  target_link_libraries(app PRIVATE ${HEARABLES_APP_LIB})
else()
  target_sources(app PRIVATE main.cc)
endif()
