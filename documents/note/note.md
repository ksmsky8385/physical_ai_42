
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
```