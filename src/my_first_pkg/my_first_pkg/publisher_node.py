import rclpy # import the rclpy library, which is the ROS 2 client library for Python
from rclpy.node import Node # import the Node class from rclpy.node, which is the base class for creating ROS 2 nodes
from std_msgs.msg import String # import the String message type from the std_msgs package, which is used for publishing and subscribing to string messages

class PublishNode(Node): # define a new class called PublishNode that inherits from the Node class
    def __init__(self): # define the constructor for the PublishNode class
        super().__init__('publish_node') # call the constructor of the parent Node class and give the node a name 'publish_node'
        self.publisher_ = self.create_publisher(String, 'hello_topic', 10) # create a publisher that will publish messages of type String to the topic named 'hello_topic' with a queue size of 10
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback) # create a timer that will call the timer_callback function every 1 second
        self.i = 0 # initialize a counter variable to keep track of the number of messages published

    def timer_callback(self): # define the callback function that will be called by the timer
        msg = String() # create a new String message
        msg.data = f'Hello, ROS 2! {self.i}' # set the data field of the message
        self.publisher_.publish(msg) # publish the message
        self.get_logger().info(f'Publishing: "{msg.data}"') # log the published message
        self.i += 1 # increment the counter
        
def main(args=None): # define the main function that will be executed when the script is run
    rclpy.init(args=args) # initialize the ROS 2 Python client library with any command-line arguments passed to the script
    node = PublishNode() # create an instance of the PublishNode class, which initializes the node and sets up the publisher and timer
    rclpy.spin(node) # keep the node running and processing callbacks until it is shut down
    node.destroy_node() # destroy the node to clean up resources
    rclpy.shutdown() # shut down the ROS 2 Python client library

if __name__ == '__main__': # check if the script is being run directly (not imported as a module)
    main() # call the main function to start the node