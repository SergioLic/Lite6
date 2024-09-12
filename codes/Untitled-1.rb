
        positions = [
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6],  # Home
            [82.7, -4.6, 101, 0, 90, 0],  # Pick  

            [101.4, 0.1, 83.4, -3.4, 79.8, 14],  # PG
            #gripper close
            [101.4, 0.1, 111.2, -3.4, 79.8, 14], # Lift PG
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [141.5, 52.7, 96.5, 5.6, 38.6, 81], # Place PG
            #gripper open
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [153.4, -5.3, 136.6, 0.9, 41.1, 49.3], #Control lift
            [82.7, -4.6, 101, 0, 90, 0],  # Pick  
            [82.5, 0.7, 84.2, -7.4, 77, -7.9],  # J
            #gripper close
            [82.6, -7.4, 88.3, -10.5, 74, -8.2], # Lift J
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [138.3, 38.9, 74.1, 14.8, 31.5, 69.2], # Place J
            #gripper open
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [82.7, -4.6, 101, 0, 90, 0],  # Pick
            [65.6, 7.3, 91, -2.6, 75.3, -23.9],  # Barra 
            #gripper close
            [63.7, -0.7, 95, -1.6, 72.2, -24.2], # Lift barra
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [134.9, 29.3, 59.6, 8.2, 23.7, 73.1], # Place PG
            #gripper open
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [82.7, -4.6, 101, 0, 90, 0],  # Pick
            [104.9, 22.3, 109.8, -3.1, 79.5, 17.2],  # Triángulo
            #gripper close
            [104.9, 16.7, 109.8, -4, 73, 12.2], # Lift triangulo
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [135.6, 49.8, 93.2, -4.1, 41.6, 76.6], # Place triangulo
            #gripper open
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [82.7, -4.6, 101, 0, 90, 0],  # Pick
            [95.4, 17.5, 102.8, -7.3, 67, -0.8], # Y
            #gripper close
            [95, 13.2, 103, -7.3, 63.3, 1.6], # Lift Y
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [128.6, 41.7, 80.1, 1.8, 32.2, 65.2], # Place Y
            #gripper open
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [82.7, -4.6, 101, 0, 90, 0],  # Pick
            [77.8, 27.3, 116.5, 0.1, 74.8, -14.2], # PP
            #gripper close
            [77.8, 30.1, 126.6, 1.7, 80.2, -18.3], # Lift PP
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [134.8, 58.4, 108.5, 0.5, 43.5, 74.8], # Place PP
            #gripper open
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6] # Home

            from xarm.wrapper import XArmAPI
import rclpy
from rclpy.node import Node
import time
import paho.mqtt.client as mqtt
import re

class MQTTListener(Node):
    def _init_(self):
        super()._init_('mqtt_listener')
        self.move_flag = False  
        self.stop_flag = False

        self.detected_classes = set()  
        self.required_classes = {'1', '2', '3', '4', '5', '6'}  
        
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        self.client.connect("10.50.70.34", 1883, 60)  #SF
        self.client.subscribe("detected/piece")
        
        self.client.loop_start()
    
    def on_connect(self, client, userdata, flags, rc):
        self.get_logger().info(f'Connected to MQTT broker with result code {rc}')
            
    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        self.get_logger().info(f'Received MQTT message: {message}')

        match = re.search(r'Clase: (\d+)', message)
        if match:
            detected_class = match.group(1)
            self.get_logger().info(f'Detected class: {detected_class}')
            
            if detected_class == '7':
                self.get_logger().info('Detected class 7, starting specific movement cycle for class 7')
                self.move_flag = True  
                self.move_arm_for_class_7()

            elif detected_class == '8':
                self.get_logger().info('Detected class 8, starting specific movement cycle for class 8')
                self.move_flag = True  
                self.move_arm_for_class_8()

            elif detected_class != '0':
                self.detected_classes.add(detected_class)
                self.get_logger().info(f'Classes detected so far: {self.detected_classes}')
            
            if self.required_classes.issubset(self.detected_classes):
                self.get_logger().info('All required classes detected, starting movement cycle for classes 1-6')
                self.move_flag = True  
                self.move_arm()

    def move_arm(self):
        ip = '192.168.1.186'
        arm = XArmAPI(ip)
        arm.motion_enable(enable=True, servo_id=8)
        arm.set_mode(0)
        arm.set_state(0)

        positions = [
#PG----------------------------------------------------------------    
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6],  # Home
            [82.7, -4.6, 101, 0, 90, 0],  # Pick  
            [101.4, 0.1, 83.4, -3.4, 79.8, 14],  # PG
            #gripper close
            [101.4, 0.1, 111.2, -3.4, 79.8, 14], # Lift PG
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [141.5, 52.7, 96.5, 5.6, 38.6, 81], # Place PG
            #gripper open
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6],  # Home
#J----------------------------------------------------------------
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            #[153.4, -5.3, 136.6, 0.9, 41.1, 49.3], #Control lift
            [82.7, -4.6, 101, 0, 90, 0],  # Pick  
            [82.5, 0.7, 84.2, -7.4, 77, -7.9],  # J
            #gripper close
            [82.6, -7.4, 88.3, -10.5, 74, -8.2], # Lift J
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [138.3, 38.9, 74.1, 14.8, 31.5, 69.2], # Place J
            #gripper open
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6],  # Home
#Barra----------------------------------------------------------------
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [82.7, -4.6, 101, 0, 90, 0],  # Pick
            [65.6, 7.3, 91, -2.6, 75.3, -23.9],  # Barra 
            #gripper close
            [63.7, -0.7, 95, -1.6, 72.2, -24.2], # Lift barra
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [134.9, 29.3, 59.6, 8.2, 23.7, 73.1], # Place Barra
            #gripper open
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6],  # Home
#Triangulo----------------------------------------------------------------

            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [82.7, -4.6, 101, 0, 90, 0],  # Pick
            [104.9, 22.3, 109.8, -3.1, 79.5, 17.2],  # Triángulo
            #gripper close
            [104.9, 16.7, 109.8, -4, 73, 12.2], # Lift triangulo
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [135.6, 49.8, 93.2, -4.1, 41.6, 76.6], # Place triangulo
            #gripper open
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6],  # Home
#Y----------------------------------------------------------------

            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [82.7, -4.6, 101, 0, 90, 0],  # Pick
            [95.4, 17.5, 102.8, -7.3, 67, -0.8], # Y
            #gripper close
            [95, 13.2, 103, -7.3, 63.3, 1.6], # Lift Y
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [128.6, 41.7, 80.1, 1.8, 32.2, 65.2], # Place Y
            #gripper open
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6],  # Home
#PP----------------------------------------------------------------

            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [82.7, -4.6, 101, 0, 90, 0],  # Pick
            [77.8, 27.3, 116.5, 0.1, 74.8, -14.2], # PP
            #gripper close
            [77.8, 30.1, 126.6, 1.7, 80.2, -18.3], # Lift PP
            [137.7, 4, 96.5, 8.5, 77.9, 50], #CONTROL
            [134.8, 58.4, 108.5, 0.5, 43.5, 74.8], # Place PP
            #gripper open
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6] # Home
        ]

        speed = 45

        for position in positions:
            self.get_logger().info(f'Moving arm to position: {position}')
            arm.set_servo_angle(angle=position, speed=speed, wait=True)

            if position == [-3, 2.6, 94.5, -4.4, -1.8, 3.6]:
                arm.open_lite6_gripper()
                time.sleep(1)  
#PG----------------------------------------------------------------
            if position == [101.4, 0.1, 83.4, -3.4, 79.8, 14]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [141.5, 52.7, 96.5, 5.6, 38.6, 81]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)
#J----------------------------------------------------------------
                
            if position == [82.5, 0.7, 84.2, -7.4, 77, -7.9]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [138.3, 38.9, 74.1, 14.8, 31.5, 69.2]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)
#Barra----------------------------------------------------------------

            if position == [65.6, 7.3, 91, -2.6, 75.3, -23.9]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [134.9, 29.3, 59.6, 8.2, 23.7, 73.1]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)
#Triangulo----------------------------------------------------------------
            
            if position == [104.9, 22.3, 109.8, -3.1, 79.5, 17.2]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [135.6, 49.8, 93.2, -4.1, 41.6, 76.6]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)
#Y----------------------------------------------------------------
            
            if position == [137.7, 4, 96.5, 8.5, 77.9, 50]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [128.6, 41.7, 80.1, 1.8, 32.2, 65.2]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)

#PP----------------------------------------------------------------
            
            if position == [77.8, 27.3, 116.5, 0.1, 74.8, -14.2]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [134.8, 58.4, 108.5, 0.5, 43.5, 74.8]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)
            time.sleep(2)  

        arm.open_lite6_gripper()
        arm.disconnect()

    def move_arm_for_class_7(self):
            ip = '192.168.1.186'
            arm = XArmAPI(ip)
            arm.motion_enable(enable=True, servo_id=8)
            arm.set_mode(0)
            arm.set_state(0)

            positions_class_7 = [
                [-3, 2.6, 94.5, -4.4, -1.8, 3.6],  # Home

            ]
            speed = 45

            for position in positions_class_7:
                self.get_logger().info(f'Moving arm to position for class 7: {position}')
                arm.set_servo_angle(angle=position, speed=speed, wait=True)
                time.sleep(2)

            arm.open_lite6_gripper()
            arm.disconnect()

    def move_arm_for_class_8(self):
        ip = '192.168.1.186'
        arm = XArmAPI(ip)
        arm.motion_enable(enable=True, servo_id=8)
        arm.set_mode(0)
        arm.set_state(0)

        positions_class_8 = [
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6],  # Home

        ]

        speed = 45

        for position in positions_class_8:
            self.get_logger().info(f'Moving arm to position for class 8: {position}')
            arm.set_servo_angle(angle=position, speed=speed, wait=True)
            time.sleep(2)

        arm.open_lite6_gripper()
        arm.disconnect()

def stop(self):
        self.stop_flag = True

def main(args=None):
    rclpy.init(args=args)

    mqtt_listener = MQTTListener()

    try:
        while rclpy.ok():
            if mqtt_listener.stop_flag:
                mqtt_listener.get_logger().info('Stopping due to stop flag')
                break
            time.sleep(1)

    except Exception as e:
        mqtt_listener.get_logger().error(f'An exception occurred: {e}')
    finally:
        mqtt_listener.stop()  
        mqtt_listener.client.loop_stop()
        mqtt_listener.client.disconnect()
        mqtt_listener.destroy_node()
        rclpy.shutdown()

if _name_ == '_main_':
    main()