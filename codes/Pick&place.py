import rclpy
from rclpy.node import Node
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import paho.mqtt.client as mqtt
import re
import time
from xarm.wrapper import XArmAPI

GOAL_COORDINATE = [-0.20, -0.83]
INITIAL_COORDINATE = [0.0, 0.0]

class MQTTListener(Node):
    def __init__(self, navigator,arm_move_flag=False,arm_move_flag_7=False,arm_move_flag_8=False):
        super().__init__('mqtt_listener')
        self.navigator = navigator
        self.move_flag = False  # For TurtleBot4
        self.stop_flag = False  # For TurtleBot4
        self.arm_move_flag = arm_move_flag  # For xArm
        self.arm_move_flag_7 = arm_move_flag_7  # For xArm
        self.arm_move_flag_8 = arm_move_flag_8  # For xArm
        
        self.detected_classes = set()  # Detected classes
        self.required_classes = {'1', '2', '3', '4', '5', '6'}

        # MQTT client setup
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to the MQTT broker
        self.client.connect("192.168.2.15", 1883, 60)
        self.client.subscribe("detected/piece")

        # Start the MQTT loop in the background
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.get_logger().info(f'Connected to MQTT broker with result code {rc}')

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        self.get_logger().info(f'Received MQTT message: {message}')

        # Extract the detected class using regex
        match = re.search(r'Clase: (\d+)', message)
        if match:
            detected_class = match.group(1)
            self.get_logger().info(f'Detected class: {detected_class}')

            # if detected_class == '9':
            #     self.get_logger().info('Detected class 9, starting TurtleBot movement')

            if detected_class == "7":
                self.get_logger().info(f'Detected class: {detected_class}')
                self.move_flag = True  # Start TurtleBot movement
                self.stop_flag = False
                self.arm_move_flag_7 = True   

            if detected_class=="8":
                self.get_logger().info(f'Detected class: {detected_class}')
                self.move_flag = True  # Start TurtleBot movement
                self.stop_flag = False
                self.arm_move_flag_8 = True
            # if detected_class in {'7', '8'} or detected_class != '0':
            #     self.detected_classes.add(detected_class)
            #     self.get_logger().info(f'Classes detected so far: {self.detected_classes}')

            if self.required_classes.issubset(self.detected_classes):
                self.get_logger().info('All required classes detected, starting xArm movement')
                self.move_flag = True  # Start TurtleBot movement
                self.stop_flag = False
                self.arm_move_flag = True
    
    def move_arm(self):
            ip = '192.168.2.186'
            arm = XArmAPI(ip)
            arm.motion_enable(enable=True, servo_id=8)
            arm.set_mode(0)
            arm.set_state(0)

            positions = [
    #PG----------------------------------------------------------------    
                # Home
                [90,0,180,-90,-5,10],
                #1
                #Pick
                [50,20,130,0,80,0],
                #Pacman Grande  
                [62.7,8,92.4,1.3,79.5,-8.7],
                #Gripper close
                #Pacman grande arriba
                [62.7,-5.8,92.4,-0.7,79.3,-9.6],
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
                #dejar pacman
                [142.7, 56, 105.3, -0.1, 49.3, 85.2],
                #open gripper
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
    #J----------------------------------------------------------------
                #2
                #Pick
                [50,20,130,0,80,0],
                #Jota
                [45.6,14.4,99.5,-2.4,77.5,-24.1],
                #Jota arriba
                [45.6,5.1,99.5,-3.3,74.6,-24.5],
                #close gripper  
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
                #dejar jota
                [142.3,41.5,81.2,2.8,39.8,84.4],
                #open gripper
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
    #Barra----------------------------------------------------------------
                #3
                #Pick
                [50,20,130,0,80,0],
                #barra
                [34.6,24,112.3,0.8,75.6,-37.5],
                #close gripper
                #barra arriba
                [34.6,23.1,117.6,-1.6,77.2,-35.4],
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8], 
                #dejar barra
                [137.9, 33.2, 68.1, -0.2, 35.9, 85],
                #open gripper
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
    #Triangulo----------------------------------------------------------------
                #4
                #Pick
                [50,20,130,0,80,0],
                #dejar triangulo
                [71.6, 25.6, 114.8, -3.6, 77.7, -7.4],
                #close gripper
                #triangulo arriba
                [68.5,19.7,111.5,1.9,73.6,-8.4],
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
                #dejar triangulo
                [133.5,49.1,93.1,3.2,41.1,68.7],
                #open gripper
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
    #Y----------------------------------------------------------------
                #5
                #Pick
                [50,20,130,0,80,0], 
                #ye
                [60.2,35.8,129,0.6,80.8,-18.8],
                #gripper close
                #ye arriba
                [60.1,32.1,129.2,-0.6,78.4,-18.6],
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
                #dejar ye
                [132,41.8,82,-9,34.5,77.5],
                #open gripper
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
    #PP----------------------------------------------------------------
                #6
                #pick
                [50,20,130,0,80,0],
                #packman chico
                [45,37.6,130,10.7,66.8,-32.8],
                #gripper close
                #packman chico arriba
                [45,37.6,133,10.7,66.8,-32.2],
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
                #dejar packman chico
                [136,53.9,100.3,-5.8,33.4,80.9],
                #open gripper
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
                #Home
                [90,0,180,-90,-5,10]
            ]

            speed = 30

            for position in positions:
                self.get_logger().info(f'Moving arm to position: {position}')
                arm.set_servo_angle(angle=position, speed=speed, wait=True)

                if position == [50,20,130,0,80,0]:
                    arm.open_lite6_gripper()
                    time.sleep(1)  
    #PG----------------------------------------------------------------
                if position == [62.7,8,92.4,1.3,79.5,-8.7]:
                    self.get_logger().info('Reached grip position, closing gripper')
                    arm.close_lite6_gripper()
                    time.sleep(1)

                if position == [142.7, 56, 105.3, -0.1, 49.3, 85.2]:
                    self.get_logger().info('Reached place position, opening gripper')
                    arm.open_lite6_gripper()
                    time.sleep(1)
    #J----------------------------------------------------------------
                    
                if position == [45.6,14.4,99.5,-2.4,77.5,-24.1]:
                    self.get_logger().info('Reached grip position, closing gripper')
                    arm.close_lite6_gripper()
                    time.sleep(1)

                if position == [142.3,41.5,81.2,2.8,39.8,84.4]:
                    self.get_logger().info('Reached place position, opening gripper')
                    arm.open_lite6_gripper()
                    time.sleep(1)
    #Barra----------------------------------------------------------------

                if position == [34.6,24,112.3,0.8,75.6,-37.5]:
                    self.get_logger().info('Reached grip position, closing gripper')
                    arm.close_lite6_gripper()
                    time.sleep(1)

                if position == [137.9, 33.2, 68.1, -0.2, 35.9, 85]:
                    self.get_logger().info('Reached place position, opening gripper')
                    arm.open_lite6_gripper()
                    time.sleep(1)
    #Triangulo----------------------------------------------------------------
                
                if position == [71.6, 25.6, 114.8, -3.6, 77.7, -7.4]:
                    self.get_logger().info('Reached grip position, closing gripper')
                    arm.close_lite6_gripper()
                    time.sleep(1)

                if position == [133.5,49.1,93.1,3.2,41.1,68.7]:
                    self.get_logger().info('Reached place position, opening gripper')
                    arm.open_lite6_gripper()
                    time.sleep(1)
    #Y----------------------------------------------------------------
                
                if position == [60.2,35.8,129,0.6,80.8,-18.8]:
                    self.get_logger().info('Reached grip position, closing gripper')
                    arm.close_lite6_gripper()
                    time.sleep(1)

                if position == [132,41.8,82,-9,34.5,77.5]:
                    self.get_logger().info('Reached place position, opening gripper')
                    arm.open_lite6_gripper()
                    time.sleep(1)

    #PP----------------------------------------------------------------
                
                if position == [45,37.6,130,10.7,66.8,-32.8]:
                    self.get_logger().info('Reached grip position, closing gripper')
                    arm.close_lite6_gripper()
                    time.sleep(1)

                if position == [136,53.9,100.3,-5.8,33.4,80.9]:
                    self.get_logger().info('Reached place position, opening gripper')
                    arm.open_lite6_gripper()
                    time.sleep(1)
                time.sleep(1)  

            arm.open_lite6_gripper()
            arm.disconnect()
        
    def move_arm_for_class_7(self): #Huevo
                ip = '192.168.2.186'
                arm = XArmAPI(ip)
                arm.motion_enable(enable=True, servo_id=8)
                arm.set_mode(0)
                arm.set_state(0)

                positions_class_7 = [
                    #1
                    #Pick
                    [50,20,130,0,80,0],  
                    #Huevo agarrar
                    [49.1, 23.2, 115.1, 2.6, 77.6, -23.7],
                    #Gripper close

                    #Huevo arriba
                    [49.1, 14.2, 115.1, 1.9, 77.6, -23.3],
                    #control arriba
                    [128.1,6.8,107.3,3,74.5,5.8],
                    #Dejar huevo
                    [124.7, 60, 115.1, 2.1, 41.0, -58.7],
                    #Gripper open
                    [90,0,180,-90,-5,10]

                ]
                speed = 30

                for position in positions_class_7:
                    self.get_logger().info(f'Moving arm to position for class 7: {position}')
                    arm.set_servo_angle(angle=position, speed=speed, wait=True)
                    time.sleep(1)

                    if position == [49.1, 23.2, 115.1, 2.6, 77.6, -23.7]:
                        arm.close_lite6_gripper()
                        time.sleep(1)

                    if position == [124.7, 60, 115.1, 2.1, 41, -58.7]:
                        arm.open_lite6_gripper()
                        time.sleep(1)
                    

                arm.open_lite6_gripper()
                arm.disconnect()
                
    def move_arm_for_class_8(self): #Digitos
            ip = '192.168.2.186'
            arm = XArmAPI(ip)
            arm.motion_enable(enable=True, servo_id=8)
            arm.set_mode(0)
            arm.set_state(0)

            positions_class_8 = [
                #1
                #Pick
                [50,20,130,0,80,0],  # Home
                #Digitos agarrar
                [50.6, 22, 110.3, 1.6, 75.9, 16.7],
                #Gripper close

                #Digitos arriba
                [50.6, 11, 110.4, -3.5, 75.4, 16.3],
                #control arriba
                [128.1,6.8,107.3,3,74.5,5.8],
                #Dejar digitos
                [147.9, 74, 138.5, 10.4, 48.3, 95.3],
                #Gripper open
                #Home
                [90,0,180,-90,-5,10]
            ]

            speed = 30

            for position in positions_class_8:
                self.get_logger().info(f'Moving arm to position for class 8: {position}')
                arm.set_servo_angle(angle=position, speed=speed, wait=True)
                time.sleep(1)
                if position == [50.6, 22, 110.3, 1.6, 75.9, 16.7]:
                    arm.close_lite6_gripper()
                    time.sleep(1)

                if position == [147.9, 74, 138.5, 10.4, 48.3, 95.3]:
                    arm.open_lite6_gripper()
                    time.sleep(1)


            arm.open_lite6_gripper()
            arm.disconnect()

    def publish_mqtt(self, topic, message):
        # Publish an MQTT message
        self.client.publish(topic, message)
        self.get_logger().info(f'Published MQTT message on topic {topic}: {message}')

    def stop(self):
        self.stop_flag = True

def main(args=None):
    rclpy.init(args=args)

    navigator = TurtleBot4Navigator()

    # Start on dock
    if not navigator.getDockedStatus():
        navigator.info('Docking before initializing pose')
        navigator.dock()

    # Set initial pose
    initial_pose = navigator.getPoseStamped(INITIAL_COORDINATE, TurtleBot4Directions.NORTH)
    navigator.setInitialPose(initial_pose)

    # Wait for Nav2
    navigator.waitUntilNav2Active()

    # Undock
    navigator.undock()

    # Create an MQTTListener node
    mqtt_listener = MQTTListener(navigator)

    try:
        # Set goal pose for TurtleBot4
        goal_pose = navigator.getPoseStamped(GOAL_COORDINATE, TurtleBot4Directions.NORTH)

        while rclpy.ok():
            if mqtt_listener.stop_flag:
                navigator.info('Stopping cycle due to stop flag')
                break

            if mqtt_listener.move_flag:
                # Move TurtleBot4 to goal_pose
                navigator.info('Moving to goal_pose')
                navigator.startToPose(goal_pose)
                mqtt_listener.move_flag = False  # Reset flag after movement starts

                result = navigator.getResult()

                time.sleep(5)

                if result == TaskResult.SUCCEEDED:
                    mqtt_listener.publish_mqtt("robot/arrival_status", "Arrived at goal_pose")
                    mqtt_listener.get_logger().info("Robot arrived at goal_pose")

                # Wait for MQTT signal for xArm to move
                if mqtt_listener.arm_move_flag:
                    mqtt_listener.get_logger().info("Starting xArm movement based on detected class")
                    mqtt_listener.move_arm()
                    mqtt_listener.arm_move_flag=False

                if mqtt_listener.arm_move_flag_7:
                    mqtt_listener.get_logger().info("Starting xArm movement based on detected class")
                    mqtt_listener.move_arm_for_class_7()
                    mqtt_listener.arm_move_flag_7=False

                if mqtt_listener.arm_move_flag_8:
                    mqtt_listener.get_logger().info("Starting xArm movement based on detected class")
                    mqtt_listener.move_arm_for_class_8()
                    mqtt_listener.arm_move_flag_8=False

                # Return to initial_pose
                navigator.info('Returning to initial_pose')
                initial_pose = navigator.getPoseStamped(INITIAL_COORDINATE, TurtleBot4Directions.NORTH)
                navigator.startToPose(initial_pose)

                if result == TaskResult.SUCCEEDED:
                    mqtt_listener.publish_mqtt("robot/arrival_status", "Arrived at initial_pose")
                    mqtt_listener.get_logger().info("Robot returned to initial_pose")

            time.sleep(1)

    except Exception as e:
        navigator.error(f'An exception occurred: {e}')
    finally:
        mqtt_listener.stop()  # Ensure that MQTT loop is stopped
        mqtt_listener.client.loop_stop()
        mqtt_listener.client.disconnect()
        mqtt_listener.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
