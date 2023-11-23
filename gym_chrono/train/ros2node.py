import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # Replace with the appropriate message type for your publisher
from chrono_ros_interfaces.msg import Body
import argparse
import sys

class ListenerNode(Node):
    def __init__(self, cpu_id):
        super().__init__('listener_node_cpu_' + str(cpu_id))
        self.cpu_id = cpu_id

        # Subscriber
        self.subscription = self.create_subscription(
            Body,
            '/chrono_ros_node/output/cobra/state_' + str(cpu_id),
            self.listener_callback,
            10)
        self.subscription  # Prevent unused variable warning

        # Publisher
        self.publisher = self.create_publisher(
            String,  # Change the message type if needed
            '/state_received_' + str(cpu_id),  # Change to your desired topic
            10)

    def listener_callback(self, msg):
        # self.get_logger().info(f'CPU {self.cpu_id}: Heard: {msg}')
        # Example of publishing a response message
        response_msg = String()
        response_msg.data = f'Response from CPU {self.cpu_id}'
        self.publisher.publish(response_msg)

    def publish_message(self, message):
        msg = String()  # Change the message type if needed
        msg.data = message
        self.publisher.publish(msg)

def main(args=None):
    parser = argparse.ArgumentParser(description='ROS 2 Listener Node with CPU ID')
    parser.add_argument('cpu_id', type=int, help='CPU ID for the listener node')
    args = parser.parse_args()

    rclpy.init(args=sys.argv)
    cpu_id = args.cpu_id
    listener_node = ListenerNode(cpu_id)

    # Example of publishing an initial message
    listener_node.publish_message("Initial message from CPU " + str(cpu_id))

    rclpy.spin(listener_node)

    # Destroy the node explicitly
    listener_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
