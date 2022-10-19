import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, PointStamped, TransformStamped
from tf2_ros import TransformBroadcaster
import tf_transformations

agent_list = list()

class Agent():
    def __init__(self, parent, id):
        self.id = id
        self.pose = Pose()
        self.parent = parent
        self.sub_pose_ = self.parent.create_subscription(PointStamped, self.id + '/driver/gps', self.gtpose_callback, 10)
        self.publisher_ = self.parent.create_publisher(Pose, self.id + '/pose', 10)

    def gtpose_callback(self, msg):
        self.pose.position.x = msg.point.x
        self.pose.position.y = msg.point.y
        self.pose.position.z = msg.point.z
        self.publisher_.publish(self.pose)

        t = TransformStamped()
        # Read message content and assign it to
        # corresponding tf variables
        t.header.stamp = self.parent.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = self.id
        t.transform.translation.x = msg.point.x
        t.transform.translation.y = msg.point.y
        t.transform.translation.z = msg.point.z

        q = tf_transformations.quaternion_from_euler(0, 0, 0)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        self.parent.br.sendTransform(t)

class ViconWebots(Node):

    def __init__(self):
        super().__init__('vicon_webots')
        self.declare_parameter('agents', 'robot01')

        # Initialize the transform broadcaster
        self.br = TransformBroadcaster(self)

        self.initialize()
        

    def initialize(self):
        self.get_logger().info('Vicon Webots::inicialize() ok.')
        aux = self.get_parameter('agents').get_parameter_value().string_value
        id_array =  aux.split(', ')
        for i in range(int(len(id_array)),0,-1):
            agent_str = id_array[i-1]
            robot = Agent(self, agent_str)
            agent_list.append(robot)
        


def main(args=None):
    rclpy.init(args=args)
    vicon_webots = ViconWebots()
    rclpy.spin(vicon_webots)

    vicon_webots.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()