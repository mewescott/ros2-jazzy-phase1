import rclpy  # import the ROS 2 Python client library
import rclpy.node # import the Node class from rclpy
from example_interfaces.srv import AddTwoInts # import the AddTwoInts service type from the example_interfaces package

class AddTwoIntsServer(rclpy.node.Node): # define a class that inherits from the Node class
    def __init__(self): # define the constructor for the class
        super().__init__('add_two_ints_server') # call the constructor of the parent class and give the node a name
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback) # create a service with the AddTwoInts service type, the name 'add_two_ints', and the callback function add_two_ints_callback

    def add_two_ints_callback(self, request, response): # define the callback function for the service
        response.sum = request.a + request.b # calculate the sum of the two integers in the request and store it in the response
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}, sum={response.sum}') # log the incoming request and the calculated sum
        return response # return the response to the client
    
def main(args=None): # define the main function that will be called when the script is run
    rclpy.init(args=args) # initialize the ROS 2 Python client library
    add_two_ints_server = AddTwoIntsServer() # create an instance of the AddTwoIntsServer class
    rclpy.spin(add_two_ints_server) # keep the node running and processing incoming requests until it is shut down
    rclpy.shutdown() # shut down the ROS 2 Python client library when the node is shut down
    
if __name__ == '__main__': # check if the script is being run directly (not imported as a module)
    main() # call the main function to start the node