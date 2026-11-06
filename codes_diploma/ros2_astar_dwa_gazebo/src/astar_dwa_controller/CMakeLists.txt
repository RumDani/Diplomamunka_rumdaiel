cmake_minimum_required(VERSION 3.8)
project(astar_dwa_controller)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(tf2_ros REQUIRED)

add_executable(astar_dwa_node src/astar_dwa_node.cpp)
ament_target_dependencies(astar_dwa_node rclcpp geometry_msgs nav_msgs sensor_msgs visualization_msgs tf2_ros)

install(TARGETS astar_dwa_node DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY config launch rviz DESTINATION share/${PROJECT_NAME})
ament_get_python_install_dir(PYTHON_INSTALL_DIR)
set(PYTHON_REFERENCE_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/../../..")
ament_python_install_module("${PYTHON_REFERENCE_SOURCE}/robot.py" DESTINATION_SUFFIX codes_diploma)
install(FILES "${PYTHON_REFERENCE_SOURCE}/DWA.py" "${PYTHON_REFERENCE_SOURCE}/DWA+A.py"
  DESTINATION "${PYTHON_INSTALL_DIR}/codes_diploma")
install(DIRECTORY "${PYTHON_REFERENCE_SOURCE}/astar_project/"
  DESTINATION "${PYTHON_INSTALL_DIR}/codes_diploma/astar_project"
  FILES_MATCHING PATTERN "*.py" PATTERN "tests" EXCLUDE PATTERN "results" EXCLUDE)
if(BUILD_TESTING)
  enable_testing()
  add_executable(test_path_tracking test/test_path_tracking.cpp)
  add_test(NAME path_tracking COMMAND test_path_tracking)
endif()
ament_package()
