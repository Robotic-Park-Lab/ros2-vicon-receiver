#include <cstdio>
#include <chrono>
#include <array>
#include <cstring>
#include <iostream>
#include <fstream>
#include <time.h>
#include <chrono>
#include <functional>
#include <vector>
#include <typeinfo>
#include <rclcpp/rclcpp.hpp>
#include <rclcpp/logger.hpp>
#include <std_msgs/msg/bool.hpp>
#include <std_msgs/msg/float64.hpp>
#include <std_msgs/msg/float64_multi_array.hpp>
#include <std_msgs/msg/string.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <geometry_msgs/msg/quaternion.hpp>

using namespace std::chrono_literals;

/* This example creates a subclass of Node and uses std::bind() to register a
* member function as a callback from the timer. */

class ViconGazebo : public rclcpp::Node
{
  public:
    ViconGazebo() : Node("vicon_gazebo"){}
    bool initialize();
    bool iterate();

  private:
    rclcpp::Publisher<geometry_msgs::msg::Pose>::SharedPtr vicon_pose_, cf_pose_;

    rclcpp::Subscription<geometry_msgs::msg::Pose>::SharedPtr gazebo_pose_;

    std::string robotid;
    geometry_msgs::msg::Pose gt_pose;

    void gazeboposeCallback(const geometry_msgs::msg::Pose::SharedPtr msg);
};
