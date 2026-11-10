import rclpy                # import the rclpy library, which is the ROS 2 client library for Python
from rclpy.node import Node # import the Node class from rclpy.node, which is the base class for creating ROS 2 nodes

class SimpleNode(Node):  # define a new class called SimpleNode that inherits from the Node class
    def __init__(self): # define the constructor for the SimpleNode class
        super().__init__('simple_node') # call the constructor of the parent Node class and give the node a name 'simple_node'
        self.get_logger().info('Hello ROS 2! This is a simple node.') # log an informational message to indicate that the node has been initialized
        
def main(args=None): # define the main function that will be executed when the script is run 
    rclpy.init(args=args) # initialize the ROS 2 Python client library with any command-line arguments passed to the script
    node = SimpleNode() # create an instance of the SimpleNode class, which initializes the node and logs the message
    rclpy.spin(node) # keep the node running and processing callbacks until it is shut down
    node.destroy_node() # destroy the node to clean up resources
    rclpy.shutdown() # shut down the ROS 2 Python client library
    
if __name__ == '__main__': # check if the script is being run directly (not imported as a module)
    main() # call the main function to start the node