from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument # import the DeclareLaunchArgument class from launch.actions
from launch.substitutions import LaunchConfiguration # import the LaunchConfiguration class from launch.substitutions
from launch.actions import GroupAction # import the GroupAction class from launch.actions
from launch.conditions import IfCondition # import the IfCondition class from launch.conditions
from launch.substitutions import LaunchConfiguration # import the LaunchConfiguration class from launch.substitutions


def generate_launch_description():
    robot_speed_arg = DeclareLaunchArgument(
        'robot_speed',  # Name of the launch argument
        default_value='4.0',  # Default value for the launch argument
        description='Speed of the robot'  # Description of the launch argument
    )
    robot_speed = LaunchConfiguration('robot_speed')  # Create a LaunchConfiguration for the robot_speed argument
    
    enable_callback_arg = DeclareLaunchArgument(
        'enable_callback',  # Name of the launch argument
        default_value='true',  # Default value for the launch argument
        description='Enable parameter callback'  # Description of the launch argument
    )
    enable_callback = LaunchConfiguration('enable_callback')  # Create a LaunchConfiguration for the enable_callback argument
    
   
    
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',  # Name of the launch argument
        default_value='false',  # Default value for the launch argument
        description='Use simulation time'  # Description of the launch argument
    )
    use_sim_time = LaunchConfiguration('use_sim_time')  # Create a LaunchConfiguration for the use_sim_time argument
    
    
    return LaunchDescription([
        robot_speed_arg,  # Add the launch argument to the launch description
        enable_callback_arg,  # Add the launch argument to the launch description
        use_sim_time_arg,  # Add the launch argument to the launch description
        GroupAction([   # GroupAction to group the nodes together
        Node(
            package='my_first_pkg',
            executable='parameter_example',
            namespace = 'robot1',  # Set the namespace for the node
            name='parameter_node',
            parameters=[{'robot_speed': robot_speed, 'use_sim_time': use_sim_time}],  # Set the parameter values here
            output='screen'
        ),
        Node(
            package='my_first_pkg',
            executable='parameter_callback_example',
            namespace = 'robot1',  # Set the namespace for the node
            name='callback_node',
            condition=IfCondition(enable_callback),  # Only launch this node if enable_callback is true
            parameters=[{'robot_speed': robot_speed, 'use_sim_time': use_sim_time}],
            output='screen'
        ),
        ]),
    ])