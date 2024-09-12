from xarm.wrapper import XArmAPI
import rclpy
from rclpy.node import Node
import time
import paho.mqtt.client as mqtt
import re

class MQTTListener(Node):
    def __init__(self):
        super().__init__('mqtt_listener')
        self.move_flag = False  
        self.stop_flag = False  
        
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        self.client.connect("10.50.70.34", 1883, 60)  #SF
        #self.client.connect("172.23.254.194", 1883, 60) 
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
            
            if detected_class == '11':
                self.get_logger().info('Detected class "11", starting movement cycle')
                self.move_flag = True  
                self.stop_flag = False
                self.move_arm()  

    def move_arm(self):
        ip = '192.168.1.186'
        arm = XArmAPI(ip)
        arm.motion_enable(enable=True, servo_id=8)
        arm.set_mode(0)
        arm.set_state(0)

        positions = [
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6],  # Home
            [82.7, -4.6, 101, 0, 90, 0],  # Pick  
            [79.7, 0.2, 86.4, -0.5, 76.3, -105.9],  # Grip 
            [81.5, -0.1, 108.6, -2, 99, -9.7], # Lift
            [145.2, 1.9, 101.1, 3.2, 86.2, 0.1],
            [120.8, 68.4, 126.6, 6.4, 49, 33.2], # Place
            [153.4, -5.3, 136.6, 0.9, 41.1, 49.3],
            [-3, 2.6, 94.5, -4.4, -1.8, 3.6] # Home
        ]

        speed = 30

        for position in positions:
            self.get_logger().info(f'Moving arm to position: {position}')
            arm.set_servo_angle(angle=position, speed=speed, wait=True)

            if position == [-3, 2.6, 94.5, -4.4, -1.8, 3.6]:
                #self.get_logger().info('Reached grip position, closing gripper')
                arm.open_lite6_gripper()
                time.sleep(1)  # Wait for the gripper to close
            
            # Check if the current position is the 'grip' position
            if position == [81.5, 18.9, 108.6, -0.6, 84.5, -3]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)  # Wait for the gripper to close

            # Check if the current position is the 'grip' position
            if position == [120.8, 68.4, 126.6, 6.4, 49, 33.2]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)  # Wait for the gripper to close

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

if __name__ == '__main__':
    main()
