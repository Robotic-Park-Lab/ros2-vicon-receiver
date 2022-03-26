#include "vicon_gazebo/ViconGazebo.hpp"
using std::placeholders::_1;

bool ViconGazebo::initialize(){
	RCLCPP_INFO(this->get_logger(),"ViconGazebo::inicialize() ok.");

  vicon_pose_ = this->create_publisher<geometry_msgs::msg::Pose>("pose", 10);
	cf_pose_ = this->create_publisher<geometry_msgs::msg::Pose>("cf_pose", 10);
  gazebo_pose_ = this->create_subscription<geometry_msgs::msg::Pose>("ground_truth", 10, std::bind(&ViconGazebo::gazeboposeCallback, this, _1));

	return true;
}

bool ViconGazebo::iterate(){
  RCLCPP_INFO_ONCE(this->get_logger(),"ViconGazebo::iterate() ok.");

  auto msg = geometry_msgs::msg::Pose();
  msg = gt_pose;

  vicon_pose_->publish(msg);
	cf_pose_->publish(msg);

  return true;
}

int main(int argc, char ** argv){
    try{
        rclcpp::init(argc, argv);
        auto vicon_gazebo_node = std::make_shared<ViconGazebo>();
        rclcpp::Rate loop_rate(100);
        vicon_gazebo_node->initialize();

        while (rclcpp::ok()){
            vicon_gazebo_node->iterate();
            rclcpp::spin_some(vicon_gazebo_node);
            loop_rate.sleep();
        }
        return 0;
    }catch (std::exception &e){
		RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Exception: %s",e.what());
	}
}

void ViconGazebo::gazeboposeCallback(const geometry_msgs::msg::Pose::SharedPtr msg){
  gt_pose.position = msg->position;
  gt_pose.orientation = msg->orientation;
}
