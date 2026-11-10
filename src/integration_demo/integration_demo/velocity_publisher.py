# Import the ROS2 client library
import rclpy
# Import Node base class for creating ROS2 nodes
from rclpy.node import Node
# Import Float32 message type for publishing velocity
from std_msgs.msg import Float32
# Import SetParametersResult for handling parameter callbacks
from rcl_interfaces.msg import SetParametersResult

# Define VelocityPublisher class that inherits from Node
class VelocityPublisher(Node):
    # Initialize the node
    def __init__(self):
        # Call parent constructor with node name
        super().__init__('velocity_publisher')
        # Declare parameter so launch-provided values can be read safely
        self.declare_parameter('robot_speed', 4.0)
        # Get the 'robot_speed' parameter value from config
        self.robot_speed = self.get_parameter('robot_speed').value
        # Register callback function to handle parameter changes
        self.add_on_set_parameters_callback(self.parameter_callback)
        # Create a publisher for Float32 messages on 'velocity' topic with queue size 10
        self.publisher_ = self.create_publisher(Float32, 'velocity', 10)
        # Create a timer that calls publish_velocity every 1.0 second
        self.timer = self.create_timer(1.0, self.publish_velocity)

    # Callback function to handle parameter changes
    def parameter_callback(self, params):
        # Iterate through all changed parameters
        for param in params:
            # Check if the parameter name is 'robot_speed'
            if param.name == 'robot_speed':
                # Validate that the value is positive and not greater than 10.0
                if param.value <= 0.0 or param.value > 10.0:
                    # Log error message
                    self.get_logger().error("Invalid value for 'robot_speed'. Must be a double between 0.0 and 10.0.")
                    # Return failure status with reason
                    return SetParametersResult(successful=False, reason="Invalid value for 'robot_speed'. Must be a double between 0.0 and 10.0.")
                else:
                    # Update the robot_speed attribute with new value
                    self.robot_speed = param.value
                    # Log info message confirming the parameter update
                    self.get_logger().info(f"Parameter 'robot_speed' set to: {param.value}")
        # Return success status after processing all parameters
        return SetParametersResult(successful=True)
    
    # Function to publish velocity message
    def publish_velocity(self):
        # Create a new Float32 message object
        msg = Float32()
        # Check if robot_speed parameter has been set
        if self.robot_speed is not None:
            # Convert robot_speed to float and assign to message data
            msg.data = float(self.robot_speed)
        else:
            # Set default velocity to 0.0
            msg.data = 0.0
            # Log warning message about missing parameter
            self.get_logger().warn("Parameter 'robot_speed' is not set. Publishing 0.0 as velocity.")
            # Exit the function early
            return
        # Publish the velocity message to the 'velocity' topic
        self.publisher_.publish(msg)
        # Log the published velocity value
        self.get_logger().info(f'Publishing velocity: {msg.data}')

# Main entry point function        
def main(args=None):
    # Initialize the ROS2 client library
    rclpy.init(args=args)
    # Create an instance of the VelocityPublisher node
    velocity_publisher = VelocityPublisher()
    # Spin the node to process callbacks and timers
    rclpy.spin(velocity_publisher)
    # Destroy the node and clean up resources
    velocity_publisher.destroy_node()
    # Shutdown the ROS2 client library
    rclpy.shutdown()
    
# Entry point guard
if __name__ == '__main__':
    # Call main function
    main()
            