import rclpy

from rclpy.node import Node
from geometry_msgs.msg import Pose, PoseWithCovariance
from nav_msgs.msg import Odometry

agent_list = list()

class Agent():
    def __init__(self, parent, id):
        self.id = id
        self.pose = Pose()
        self.parent = parent
        self.sub_pose_ = self.parent.create_subscription(Odometry, self.id + '/ground_truth', self.gtpose_callback, 10)
        self.publisher_ = self.parent.create_publisher(Pose, self.id + '/pose', 10)

    def gtpose_callback(self, msg):
        msg_aux = PoseWithCovariance()
        msg_aux = msg.pose
        self.pose = msg_aux.pose
        self.publisher_.publish(msg_aux.pose)


class ViconGazebo(Node):
    def __init__(self):
        super().__init__('vicon_gazebo')
        self.declare_parameter('agents', 'robot01')
        self.initialize()

    def initialize(self):
        self.get_logger().info('Vicon Gazebo::inicialize() ok.')
        aux = self.get_parameter('agents').get_parameter_value().string_value
        id_array =  aux.split(', ')
        for i in range(int(len(id_array)),0,-1):
            agent_str = id_array[i-1]
            robot = Agent(self, agent_str)
            agent_list.append(robot)


def main(args=None):
    rclpy.init(args=args)
    vicon_gazebo = ViconGazebo()
    rclpy.spin(vicon_gazebo)

    vicon_gazebo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()