import rclpy
import rclpy.node
from example_interfaces.srv import AddTwoInts

class AddTwoIntsClient(rclpy.node.Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()
        self.req.a = 5
        self.req.b = 3
        
        self.future = self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)
    add_two_ints_client = AddTwoIntsClient()
    rclpy.spin_until_future_complete(add_two_ints_client, add_two_ints_client.future)
    
    if add_two_ints_client.future.done():
        try:
            response = add_two_ints_client.future.result()
            add_two_ints_client.get_logger().info(f'Result of add_two_ints: {response.sum}')
        except Exception as e:
            add_two_ints_client.get_logger().error(f'Service call failed: {e}')
    
    add_two_ints_client.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()