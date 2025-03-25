cmake_minimum_required(VERSION 3.10)
project(LasapInterface)

set(CMAKE_CXX_STANDARD 17)

# Add library
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cpp)
add_library(lasap_interface STATIC ${sources})
target_include_directories(lasap_interface PUBLIC ${PROJECT_SOURCE_DIR}/include)

# Install directives
install(TARGETS lasap_interface DESTINATION "$ENV{HOME}/.local/lib")
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.h)
install(FILES ${headers} DESTINATION "$ENV{HOME}/.local/include/Lasap")

# Uninstall directive
add_custom_target(uninstall COMMAND ${CMAKE_COMMAND} -P ${PROJECT_SOURCE_DIR}/uninstall.cmake)
