# Import ROS2 client library and core modules
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import signal
import threading
import traceback


class DemoShutdownError(Exception):
    """Expected demo exception used to exercise graceful shutdown behavior."""

class SafeShutdownNode(Node):
    """
    A ROS2 node that demonstrates safe shutdown handling.
    Publishes velocity commands to a turtle and implements graceful error handling.
    """
    def __init__(self):
        # Initialize the node with a unique name
        super().__init__('safe_shutdown_demo')
        self.get_logger().info("Safe Shutdown Demo Node has been started.")

        # Create a publisher for the /cmd_vel topic to control the turtle
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Create a timer that calls control_loop every 1.0 second
        self.timer = self.create_timer(1.0, self.control_loop)
        # Initialize counter for incrementing velocity commands
        self.count = 0
        self.get_logger().info("Controller initialized")
        

    def control_loop(self):
        """Periodic callback that publishes velocity commands. Simulates an error at count=5."""
        # Simulate an error condition after 5 iterations for testing shutdown handling
        if self.count == 5:
            raise DemoShutdownError("Simulated error for safe shutdown.")
        
        # Create a Twist message for velocity commands
        msg = Twist()
        # Set linear velocity proportional to count
        msg.linear.x = 0.1 * self.count
        # Set angular velocity proportional to count
        msg.angular.z = 0.1 * self.count
        
        # Publish the velocity command
        self.publisher_.publish(msg)
        self.get_logger().info(f"Moving count: {self.count}")
        # Increment counter for next iteration
        self.count += 1
        
    def stop_robot(self):
        """Sends a zero velocity command to stop the robot safely."""
        # Create a Twist message with zero velocities
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        # Publish the stop command
        self.publisher_.publish(msg)
        self.get_logger().info("Robot stopped safely.")
        
    def cleanup(self):
        """Cleans up ROS2 resources and destroys the node."""
        # Destroy the timer to stop periodic callbacks
        self.destroy_timer(self.timer)
        # Destroy the node
        self.destroy_node()
        self.get_logger().info("Node cleaned up and shut down safely.")
        
def main(args=None):
    """Main entry point for the safe shutdown demo."""
    # Initialize the ROS2 client library
    rclpy.init(args=args)
    # Create an instance of the SafeShutdownNode
    node = SafeShutdownNode()
    shutdown_event = threading.Event()

    # Keep original handlers so we can restore them during shutdown.
    previous_sigint = signal.getsignal(signal.SIGINT)
    previous_sigterm = signal.getsignal(signal.SIGTERM)

    def handle_shutdown_signal(signum, _frame):
        """Minimal OS signal handler: set a flag and let main loop exit cleanly."""
        if shutdown_event.is_set():
            return
        signal_name = signal.Signals(signum).name
        print(f"Received {signal_name}. Requesting graceful shutdown...")
        shutdown_event.set()

    signal.signal(signal.SIGINT, handle_shutdown_signal)
    signal.signal(signal.SIGTERM, handle_shutdown_signal)
    
    try:
        # Process callbacks while watching for shutdown requests.
        while rclpy.ok() and not shutdown_event.is_set():
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        # Fallback in case KeyboardInterrupt is raised directly.
        node.get_logger().info("KeyboardInterrupt received. Stopping the robot and shutting down.")
        shutdown_event.set()
    except DemoShutdownError as e:
        # Expected lesson/demo path: concise message and graceful exit.
        node.get_logger().error(f"Runtime error triggered safe shutdown: {e}")
        shutdown_event.set()
    except Exception as e:
        # Unexpected runtime failures should include traceback for debugging.
        node.get_logger().error(f"Unexpected runtime error: {e}")
        node.get_logger().error(traceback.format_exc())
        shutdown_event.set()
    finally:
        # Restore default signal behavior.
        try:
            signal.signal(signal.SIGINT, previous_sigint)
            signal.signal(signal.SIGTERM, previous_sigterm)
        except Exception as e:
            node.get_logger().error(f"Failed to restore signal handlers: {e}")
            node.get_logger().error(traceback.format_exc())

        # Ensure cleanup happens regardless of how the node exits.
        try:
            node.stop_robot()
        except Exception as e:
            node.get_logger().error(f"Shutdown error while stopping robot: {e}")
            node.get_logger().error(traceback.format_exc())

        try:
            node.cleanup()
        except Exception as e:
            node.get_logger().error(f"Shutdown error during node cleanup: {e}")
            node.get_logger().error(traceback.format_exc())

        # Shutdown ROS2
        try:
            if rclpy.ok():
                rclpy.shutdown()
        except Exception as e:
            node.get_logger().error(f"Shutdown error during rclpy.shutdown(): {e}")
            node.get_logger().error(traceback.format_exc())

        print("ROS2 node has been shut down safely.")
        
if __name__ == '__main__':
    main()