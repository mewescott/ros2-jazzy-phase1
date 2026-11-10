import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSDurabilityPolicy, QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

class QoSTestNode(Node):
    def __init__(self):
        super().__init__('qos_publisher')
        self.get_logger().info("QoS Test Node has been started.")

        # Define a QoS profile with BEST_EFFORT reliability and KEEP_LAST history
        qos_profile = QoSProfile(
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Create a publisher with the defined QoS profile
        self.publisher_ = self.create_publisher(String, 'qos_topic', qos_profile)
        self.timer = self.create_timer(1.0, self.publish_message)
        self.counter = 0

    def publish_message(self):
        msg = String()
        msg.data = f"Hello from QoS Test Node! Counter: {self.counter}"
        self.publisher_.publish(msg)
        self.counter += 1
        self.get_logger().info(f"Published message: {msg.data}")
        
        
def main(args=None):
    rclpy.init(args=args)
    qos_test_node = QoSTestNode()
    rclpy.spin(qos_test_node)
    qos_test_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()