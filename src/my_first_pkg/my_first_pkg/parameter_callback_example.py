import rclpy # import the ROS 2 Python client library
import rclpy.node # import the Node class from rclpy
from rclpy.parameter import Parameter   # import Parameter from rclpy.parameter to use in the parameter callback
from rcl_interfaces.msg import SetParametersResult # import SetParametersResult from rcl_interfaces.msg to use in the parameter callback

class ParameterCallbackExampleNode(rclpy.node.Node): # define a class that inherits from the Node class
    def __init__(self): # define the constructor for the class
        super().__init__('parameter_callback_example_node') # call the constructor of the parent class and give the node a name
        self.declare_parameter('robot_speed', 1.0) # declare a parameter named 'robot_speed' with an initial value of 1.0
        self.get_logger().info(f"Parameter 'robot_speed' declared with value: 1.0") # log the declaration of the 'robot_speed' parameter
        
        # Add a parameter callback
        self.add_on_set_parameters_callback(self.parameter_callback)
        
        speed = self.get_parameter('robot_speed').value # get the initial value of the 'robot_speed' parameter
        self.get_logger().info(f"Initial 'robot_speed' value: {speed}") # log the initial value of the 'robot_speed' parameter

    def parameter_callback(self, params): # define the parameter callback function that will be called when parameters are set
        for param in params: # iterate through the list of parameters that are being set
            if param.name == 'robot_speed': # check if the parameter being set is 'robot_speed'
                if param.type_ == Parameter.Type.DOUBLE and 0.0 <= param.value <= 5.0: # check if the parameter is of type double and within the valid range
                    self.get_logger().info(f"Parameter 'robot_speed' set to: {param.value}") # log the new value of the 'robot_speed' parameter
                    return SetParametersResult(successful=True) # return a successful result if the parameter value is valid
                else:
                    self.get_logger().error("Invalid value for 'robot_speed'. Must be a double between 0.0 and 5.0.") # log an error message if the parameter value is invalid
                    return SetParametersResult(successful=False, reason="Invalid value for 'robot_speed'. Must be a double between 0.0 and 5.0.") # return an unsuccessful result if the parameter value is invalid
        return SetParametersResult(successful=True) # return a successful result for other parameters
    
def main(args=None): # define the main function that will be called when the script is run
    rclpy.init(args=args) # initialize the ROS 2 Python client library
    parameter_callback_example_node = ParameterCallbackExampleNode() # create an instance of the ParameterCallbackExampleNode class
    rclpy.spin(parameter_callback_example_node) # keep the node running and processing incoming requests until it is shut down
    parameter_callback_example_node.destroy_node() # destroy the node when it is shut down
    rclpy.shutdown() # shut down the ROS 2 Python client library when the node is shut down
    
if __name__ == '__main__': # check if the script is being run directly (not imported as a module)
    main() # call the main function to start the node
