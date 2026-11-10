# Import LaunchDescription class for creating launch files
from launch import LaunchDescription
# Import DeclareLaunchArgument to declare command-line arguments
from launch.actions import DeclareLaunchArgument
# Import LaunchConfiguration to reference launch arguments
from launch.substitutions import LaunchConfiguration
# Import Node action for launching ROS 2 nodes
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

# Define the function that generates the launch description
def generate_launch_description():
    pkg_share_dir = get_package_share_directory('integration_demo')  # Get the package share directory for 'integration_demo'
    params_file = os.path.join(pkg_share_dir, 'config', 'params.yaml')  # Path to the params.yaml file
    
    # Declare the launch argument 'robot_speed' with default value of 4.0 m/s
    robot_speed_arg = DeclareLaunchArgument(
        'robot_speed',  # Argument name
        default_value='4.0',  # Default value if not provided
        description='Speed of the robot'  # Description for the argument
    )
    
    # Create a LaunchConfiguration object to reference the robot_speed argument
    robot_speed = LaunchConfiguration('robot_speed')
    
    # Return the LaunchDescription containing all nodes and arguments
    return LaunchDescription([
        # Add the robot_speed argument to the launch description
        robot_speed_arg,
        # Create and launch the velocity_publisher node
        Node(
            package='integration_demo',  # Package containing the executable
            executable='velocity_publisher',  # Name of the executable to run
            namespace='robot1',  # Namespace for the node
            name='velocity_publisher',  # Name of the node
            parameters=[params_file],  # Pass robot_speed as a parameter
            output='screen'  # Direct node output to the screen
        ),
    ])