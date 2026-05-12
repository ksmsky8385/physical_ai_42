# TurtleBot 기본

```bash
ros2 launch turtlebot3_bringup robot.launch.py
```

# 카메라

```bash
# TurtleBot (카메라)
ros2 run v4l2_camera v4l2_camera_node

# 노트북
sudo apt install ros-humble-compressed-image-transport
ros2 run rqt_image_view rqt_image_view
```

# My Launch

```bash
# 1. 워크스페이스 이동
mkdir -p ~/Workspace/ros2_ws/src
cd ~/Workspace/ros2_ws/src

# 2. 파이썬 기반 패키지 생성 (의존성 포함)
ros2 pkg create --build-type ament_python my_robot_bringup --dependencies rclpy v4l2_camera turtlebot3_bringup

# 3. 런처 파일을 담을 폴더 생성
mkdir -p ~/Workspace/ros2_ws/src/my_robot_bringup/launch
```

```bash
nano ~/Workspace/ros2_ws/src/my_robot_bringup/launch/camera_robot.launch.py
```

```bash
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 1. 터틀봇3 Bringup 런처 (기존 패키지 파일 가져오기)
    tb3_launch_dir = os.path.join(get_package_share_directory('turtlebot3_bringup'), 'launch')
    
    turtlebot3_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([tb3_launch_dir, '/robot.launch.py'])
    )

    # 2. 카메라 노드 실행 설정
    camera_node = Node(
        package='v4l2_camera',
        executable='v4l2_camera_node',
        name='v4l2_camera',
        parameters=[{
            'video_device': '/dev/video0',
            'image_size': [640, 480],
            'output_encoding': 'rgb8',
        }]
    )

    return LaunchDescription([
        turtlebot3_bringup,
        camera_node
    ])
```

```bash
nano ~/Workspace/ros2_ws/src/my_robot_bringup/setup.py
```

```bash
import os # 추가
from glob import glob # 추가
from setuptools import find_packages, setup

package_name = 'my_robot_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],

...
```

```bash
# 1. 워크스페이스 루트로 이동
cd ~/Workspace/ros2_ws

# 2. 빌드
colcon build

# 3. 환경 설정 적용
source install/setup.bash

# 4. 런처 실행
ros2 launch my_robot_bringup camera_robot.launch.py
```