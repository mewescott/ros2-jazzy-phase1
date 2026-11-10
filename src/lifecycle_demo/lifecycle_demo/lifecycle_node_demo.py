import rclpy
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle import State
from rclpy.lifecycle import TransitionCallbackReturn
from std_msgs.msg import String

class ManagerNode(LifecycleNode):
    def __init__(self):
        super().__init__('managed_node')
        self.publisher_ = None
        self.timer = None
        self.counter = 0

    def on_configure(self, state: State):
        self.get_logger().info("Configuring Node...")
        self.publisher_ = self.create_lifecycle_publisher(String, 'lifecycle_topic', 10)
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State):
        self.get_logger().info("Activating Node...")
        self.timer = self.create_timer(1.0, self.publish_message)
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State):
        self.get_logger().info("Deactivating Node...")
        if self.timer is not None:
            self.destroy_timer(self.timer)
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state: State):
        self.get_logger().info("Cleaning up Node...")
        if self.publisher_ is not None:
            self.destroy_publisher(self.publisher_)
        return TransitionCallbackReturn.SUCCESS

    def publish_message(self):
        msg = String()
        msg.data = f"Lifecycle message {self.counter}"
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published: {msg.data}")
        self.counter += 1
        
def main(args=None):
    rclpy.init(args=args)
    manager_node = ManagerNode()
    rclpy.spin(manager_node)
    manager_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
