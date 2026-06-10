
``` shell
# 거북이 시뮬레이터 띄우기
ros2 run turtlesim turtlesim_node

# 새 터미널에서 키보드 조작 명령어
ros2 run turtlesim turtle_teleop_key

# 다른 터미널에서
cd ~/ros2_ws

# 전체 빌드
colcon build

# (추천) 수정 중인 특정 패키지만 빌드해서 시간을 아끼고 싶을 때
colcon build --packages-select <패키지_이름>

cd ~/workspace/physical_ai_42/ros2_ws
source install/setup.bash

ros2 run hello_ros2_pkg turtle_square

```

``` shell

ros2 pkg create --build-type ament_cmake hello_cmake_pkg --dependencies rclcpp std_msgs

```

``` shell
ssh tme@192.168.1.189

ssh tme@10.231.144.195

ssh tme@10.42.0.189


```



``` shell
ssh tme@10.143.2.12

cd Workspace/ros2_ws

source install/setup.bash

ros2 launch my_robot_bringup robot.launch.py

  use_camera:=true/false
  use_joy:=true/false
  use_twist_mux:=true/false

ros2 launch my_robot_bringup slam.launch.py
ros2 launch my_robot_bringup nav.launch.py map:="경로"
ros2 launch my_robot_bringup all.launch.py map:="경로"


```

``` shell

ros2 run camera_pkg pose_yolo

ros2 launch my_robot_nav mapping.launch.py
ros2 launch my_robot_nav nav_slam.launch.py

```

ros2 run teleop_twist_joy teleop_node --ros-args   -p require_enable_button:=false   -p axis_linear.x:=1   -p axis_angular.yaw:=0   -p scale_linear.x:=0.20   -p scale_angular.yaw:=2.0
