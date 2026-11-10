import rclpy
from rclpy.node import Node
import time
from rclpy.executors import SingleThreadedExecutor


class ExecutionDemoNode(Node):
    def __init__(self):
        super().__init__('execution_demo_node')
        self.get_logger().info("Execution Demo Node has been started.")
        self.timer2 = self.create_timer(2.0, self.timer2_callback)

        self.timer1 = self.create_timer(1.0, self.timer1_callback)
    def timer1_callback(self):
        self.get_logger().info("Timer1 callback executed.")
        time.sleep(0.5)  # Simulate some work being done in the callback
        self.get_logger().info("Timer1 callback finished execution.")
        
    def timer2_callback(self):
        self.get_logger().info("Timer 2 callback fired.")
        
        
def main(args=None):
    rclpy.init(args=args)
    execution_demo_node = ExecutionDemoNode()
    executor = SingleThreadedExecutor()
    executor.add_node(execution_demo_node)
    executor.spin()
    execution_demo_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main() 
