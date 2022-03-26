cmake_minimum_required(VERSION 3.8)
project(vicon_gazebo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

include_directories(
  include
  ${Boost_INCLUDE_DIRS}
)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rcutils)
find_package(Boost REQUIRED COMPONENTS thread)


ament_export_dependencies(rosidl_default_runtime geometry_msgs)

add_executable(vicon_gazebo src/vicon_gazebo.cpp)
ament_target_dependencies(vicon_gazebo "rclcpp" "rcutils" "geometry_msgs")
target_include_directories(vicon_gazebo PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(vicon_gazebo PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17

install(TARGETS vicon_gazebo
  DESTINATION lib/${PROJECT_NAME})


ament_package()
