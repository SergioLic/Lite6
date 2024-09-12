# from xarm.wrapper import XArmAPI
# import rclpy
# from rclpy.node import Node
# import time
# import paho.mqtt.client as mqtt
# import re
# import math
# import os
# import sys
# from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator
# from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

# #from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

# inital_pose = [0.0, 0.0]
# goal_pose = [-0.20,-0.83]
# ##################INICIAR MQTT

# class MQTTListener(Node):
#     def __init__(self, navigator):
#         super().__init__('mqtt_listener')
#         self.navigator = navigator
#         self.move_flag = False  
#         self.stop_flag = False

#         self.detected_classes = set()  
#         self.required_classes = {'1', '2', '3', '4', '5', '6'}  
        
#         self.client = mqtt.Client()
#         self.client.on_connect = self.on_connect
#         self.client.on_message = self.on_message
        
#         self.client.connect("192.168.2.15", 1883, 60)  #SF
#         self.client.subscribe("detected/piece")
        
#         self.client.loop_start()

# ###################INICIAR TURTLEBOT  

#     def navigation(navigator):
#         # Start on dock
#         navigator = TurtleBot4Navigator()

#         if not navigator.getDockedStatus():
#             navigator.info('Docking before initialising pose')
#             navigator.dock()

#         # Set initial pose
#         inicio = navigator.getPoseStamped(inital_pose, TurtleBot4Directions.NORTH)
#         navigator.setInitialPose(inicio)

#         # Wait for Nav2
#         navigator.waitUntilNav2Active()

#         mqtt_listener = MQTTListener(navigator)

#         # Set goal poses
#         final = navigator.getPoseStamped(goal_pose, TurtleBot4Directions.NORTH)

#         # Undock
#         navigator.undock()

#         # Go to each goal pose
#         #navigator.startToPose(goal_pose)

#         #rclpy.shutdown()

# #################DETECCIÓN DE CLASES

#     def on_connect(self, client, userdata, flags, rc):
#         self.get_logger().info(f'Connected to MQTT broker with result code {rc}')
            
#     def on_message(self, client, userdata, msg):
#         message = msg.payload.decode()
#         self.get_logger().info(f'Received MQTT message: {message}')

#         match = re.search(r'Clase: (\d+)', message)
#         if match:
#             detected_class = match.group(1)
#             self.get_logger().info(f'Detected class: {detected_class}')

#             if detected_class == '7':
#                 self.get_logger().info('Detected class 7, starting specific movement cycle for class 7')
#                 self.move_flag = True
#                 self.move_arm_for_class_7()

#             elif detected_class == '8':
#                 self.get_logger().info('Detected class 8, starting specific movement cycle for class 8')
#                 self.move_flag = True  
#                 self.move_arm_for_class_8()

#             elif detected_class != '0':
#                 self.detected_classes.add(detected_class)
#                 self.get_logger().info(f'Classes detected so far: {self.detected_classes}')
            
#             if self.required_classes.issubset(self.detected_classes):
#                 self.get_logger().info('All required classes detected, starting movement cycle for classes 1-6')
#                 self.move_flag = True  
#                 self.move_arm()
    
#     def move_arm(self):
#         ip = '192.168.2.186'
#         arm = XArmAPI(ip)
#         arm.motion_enable(enable=True, servo_id=8)
#         arm.set_mode(0)
#         arm.set_state(0)

#         speed = 25

#         positions = [
#                         #Home
#             [90,0,180,-90,-5,10],

#             #1
#             #pick
#             [50,20,130,0,80,0],
#             #packman grande
#             [62.7,8,92.4,1.3,79.5,-8.7],
#             #Gripper close
#             #packman grande arriba
#             [62.7,-5.8,92.4,-0.7,79.3,-9.6],
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],
#             #dejar packman grande 
#             [142.7, 56, 105.3, -0.1, 49.3, 85.2],
#             #open gripper
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],

#             #2
#             #pick
#             [50,20,130,0,80,0],
#             #jota
#             [45.6,14.4,99.5,-2.4,77.5,-24.1],
#             #jota arriba
#             [45.6,5.1,99.5,-3.3,74.6,-24.5],
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],
#             #dejar jota 
#             [142.3,41.5,81.2,2.8,39.8,84.4],
#             #open gripper
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],

#             #3
#             #pick
#             [50,20,130,0,80,0],
#             #barra
#             [34.6,24,112.3,0.8,75.6,-37.5],
#             #barra arriba
#             [34.6,23.1,117.6,-1.6,77.2,-35.4],
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],
#             #dejar barra
#             [137.9, 33.2, 68.1, -0.2, 35.9, 85],
#             #open gripper
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],

#             #4
#             #pick
#             [50,20,130,0,80,0],
#             #triangulo
#             [71.6, 25.6, 114.8, -3.6, 77.7, -7.4],
#             #triangulo arriba
#             [68.5,19.7,111.5,1.9,73.6,-8.4],
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],
#             #dejar triangulo
#             [133.5,49.1,93.1,3.2,41.1,68.7],
#             #open gripper
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],



#             #5
#             #pick
#             [50,20,130,0,80,0],
#             #ye
#             [60.2,35.8,129,0.6,80.8,-18.8],
#             #ye arriba
#             [60.1,32.1,129.2,-0.6,78.4,-18.6],
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],
#             #dejar ye
#             [132,41.8,82,-9,34.5,77.5],
#             #open gripper
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],


#             #6
#             #pick
#             [50,20,130,0,80,0],
#             #packman chico
#             [45,37.6,130,10.7,66.8,-32.8],
#             #packman chico arriba
#             [45,37.6,133,10.7,66.8,-32.2],
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],
#             #dejar packman chico
#             [136,53.9,100.3,-5.8,33.4,80.9],
#             #open gripper
#             #control arriba
#             [128.1,6.8,107.3,3,74.5,5.8],
#             #Home
#             [90,0,180,-90,-5,10]
#             ]
#         arm.set_pause_time(1)

#         for positions in positions:
#                 code = arm.set_servo_angle(angle=positions, speed=speed, wait=True)

#                 if positions == [50,20,130,0,80,0]:          
#                         arm.open_lite6_gripper()
#                         time.sleep(1)
# #PG----------------------------------------------------------------
#                 if positions == [62.7,8,92.4,1.3,79.5,-8.7]:
#                         arm.close_lite6_gripper()
#                         time.sleep(2)

#                 if positions == [142.7, 56, 105.3, -0.1, 49.3, 85.2]:
#                         arm.open_lite6_gripper()
#                         time.sleep(2)

# #J----------------------------------------------------------------
                
#                 if positions == [45.6,14.4,99.5,-2.4,77.5,-24.1]:
#                         arm.close_lite6_gripper()
#                         time.sleep(2)

#                 if positions == [142.3,41.5,81.2,2.8,39.8,84.4]:
#                         arm.open_lite6_gripper()
#                         time.sleep(2)
# #Barra----------------------------------------------------------------

#                 if positions == [34.6,24,112.3,0.8,75.6,-37.5]:
#                         arm.close_lite6_gripper()
#                         time.sleep(2)

#                 if positions == [137.9, 33.2, 68.1, -0.2, 35.9, 85]:
#                         arm.open_lite6_gripper()
#                         time.sleep(2)
# #Triangulo----------------------------------------------------------------
            
#                 if positions == [71.6, 25.6, 114.8, -3.6, 77.7, -7.4]:
#                         arm.close_lite6_gripper()
#                         time.sleep(2)

#                 if positions == [133.5,49.1,93.1,3.2,41.1,68.7]:
#                         arm.open_lite6_gripper()
#                         time.sleep(2)
# #Y----------------------------------------------------------------
            
#                 if positions == [60.2,35.8,129,0.6,80.8,-18.8]:
#                         arm.close_lite6_gripper()
#                         time.sleep(2)

#                 if positions == [132,41.8,82,-9,34.5,77.5]:
#                         arm.open_lite6_gripper()
#                         time.sleep(2)

# #PP----------------------------------------------------------------
            
#                 if positions == [45,37.6,130,10.7,66.8,-32.8]:
#                         arm.close_lite6_gripper()
#                         time.sleep(2)

#                 if positions == [136,53.9,100.3,-5.8,33.4,80.9]:
#                         arm.open_lite6_gripper()
#                         time.sleep(2)
#                 time.sleep(2)  

# #DIGITOS----------------------------------------------------------------
            
#                 if positions == [50.6, 22, 110.3, 1.6, 75.9, 16.7]:
#                         arm.close_lite6_gripper()
#                         time.sleep(2)

#                 if positions == [147.9, 74, 138.5, 10.4, 48.3, 95.3]:
#                         arm.open_lite6_gripper()
#                         time.sleep(2)
#                 time.sleep(2)  

# #HUEVO----------------------------------------------------------------
            
#                 if positions == [49.1, 23.2, 115.1, 2.6, 77.6, -23.7]:
#                         arm.close_lite6_gripper()
#                         time.sleep(2)

#                 if positions == [124.7, 60, 115.1, 2.1, 41, -58.7]:
#                         arm.open_lite6_gripper()
#                         time.sleep(2)
#                 time.sleep(2)  

#         time.sleep(2)
#         arm.open_lite6_gripper()
#         #arm.disconnect()
    
#     def move_arm_7(self): #Huevo
#           ip = '192.168.2.186'
#           arm = XArmAPI(ip)
#           arm.motion_enable(enable=True, servo_id=8)
#           arm.set_mode(0)
#           arm.set_state(0)
          
#           positions_class_7 = [
#                 #1
#                 #Pick
#                 [50,20,130,0,80,0],  
#                 #Huevo agarrar
#                 [49.1, 23.2, 115.1, 2.6, 77.6, -23.7],
#                 #Gripper close

#                 #Huevo arriba
#                 [49.1, 14.2, 115.1, 1.9, 77.6, -23.3],
#                 #control arriba
#                 [128.1,6.8,107.3,3,74.5,5.8],
#                 #Dejar huevo
#                 [124.7, 60, 115.1, 2.1, 41, -58.7],
#                 #Gripper open
#                 #Home
#                 [90,0,180,-90,-5,10]
#           ]

#           speed = 25
#           for position in positions_class_7:
#                 self.get_logger().info(f'Moving arm to position for class 7: {position}')
#                 arm.set_servo_angle(angle=positions_class_7, speed=speed, wait=True)
#                 time.sleep(2)

#                 if positions_class_7 == [50,20,130,0,80,0]:      
#                     arm.open_lite6_gripper()
#                     time.sleep(1)

#                 if positions_class_7 == [49.1, 23.2, 115.1, 2.6, 77.6, -23.7]:
#                     arm.close_lite6_gripper()
#                     time.sleep(2)

#                 if positions_class_7 == [124.7, 60, 115.1, 2.1, 41, -58.7]:
#                     arm.open_lite6_gripper()
#                     time.sleep(2)
        
#     def move_arm_8(self):
#           ip = '192.168.2.186'
#           arm = XArmAPI(ip)
#           arm.motion_enable(enable=True, servo_id=8)
#           arm.set_mode(0)
#           arm.set_state(0)
          
#           positions_class_8 = [
#                 #1
#                 #Pick
#                 [50,20,130,0,80,0],  # Home
#                 #Digitos agarrar
#                 [50.6, 22, 110.3, 1.6, 75.9, 16.7],
#                 #Gripper close

#                 #Digitos arriba
#                 [50.6, 11, 110.4, -3.5, 75.4, 16.3],
#                 #control arriba
#                 [128.1,6.8,107.3,3,74.5,5.8],
#                 #Dejar digitos
#                 [147.9, 74, 138.5, 10.4, 48.3, 95.3],
#                 #Gripper open
#                 #Home
#                 [90,0,180,-90,-5,10]
#           ]

#           speed = 25
#           for position in positions_class_8:
#                 self.get_logger().info(f'Moving arm to position for class 8: {position}')
#                 arm.set_servo_angle(angle=positions_class_8, speed=speed, wait=True)
#                 time.sleep(2)

#                 if positions_class_8 == [50,20,130,0,80,0]:      
#                     arm.open_lite6_gripper()
#                     time.sleep(1)

#                 if positions_class_8 == [50.6, 22, 110.3, 1.6, 75.9, 16.7]:
#                     arm.close_lite6_gripper()
#                     time.sleep(2)

#                 if positions_class_8 == [147.9, 74, 138.5, 10.4, 48.3, 95.3]:
#                     arm.open_lite6_gripper()
#                     time.sleep(2)
                    
#           #arm.open_lite6_gripper()
#           #arm.disconnect()  

# def stop(self):
#         self.stop_flag = True

# def main(args=None):

#     rclpy.init(args=args)
#     navigator = TurtleBot4Navigator()
#         # Set initial pose
#     inicio = navigator.getPoseStamped(inital_pose, TurtleBot4Directions.NORTH)
#     navigator.setInitialPose(inicio)

#         # Wait for Nav2
#     navigator.waitUntilNav2Active()

#         # Set goal poses
#     final = navigator.getPoseStamped(goal_pose, TurtleBot4Directions.NORTH)
#     mqtt_listener = MQTTListener(navigator)

#     try:
#         while rclpy.ok():
#             if mqtt_listener.stop_flag:
#                 mqtt_listener.get_logger().info('Stopping due to stop flag')
#                 break
#             time.sleep(1)

#     except Exception as e:
#         mqtt_listener.get_logger().error(f'An exception occurred: {e}')
#     finally:
#         mqtt_listener.stop()  
#         mqtt_listener.client.loop_stop()
#         mqtt_listener.client.disconnect()
#         mqtt_listener.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()

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
    def _init_(self, navigator):
        super()._init_('mqtt_listener')
        self.navigator = navigator
        self.move_flag = False  
        self.stop_flag = False  
        self.detected_class = None  # Para almacenar la clase detectada
        
        # Configuración del cliente MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # Conectar al broker MQTT
        self.client.connect("192.168.2.15", 1883, 60) 
        self.client.subscribe("detected/piece")
        
        # Hilo para procesar mensajes MQTT
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.get_logger().info(f'Connected to MQTT broker with result code {rc}')
        
    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        self.get_logger().info(f'Received MQTT message: {message}')

        # Extraer la clase usando expresión regular
        match = re.search(r'Clase: (\d+)', message)
        if match:
            self.detected_class = match.group(1)
            self.get_logger().info(f'Detected class: {self.detected_class}')
            
            if self.detected_class == '9':
                self.get_logger().info('Detected class "9", starting movement cycle')
                self.move_flag = True  
                self.stop_flag = False

    def publish_mqtt(self, topic, message):
        # Publicar un mensaje en el broker MQTT
        self.client.publish(topic, message)
        self.get_logger().info(f'Published MQTT message on topic {topic}: {message}')

    def stop(self):
        self.stop_flag = True

def execute_lite6_routine(listener):
    # Esta función seleccionará la rutina del Lite 6 dependiendo de la clase detectada
    if listener.detected_class == '9':
        # Ejecutar una rutina específica para la clase '9'
        listener.publish_mqtt("lite6/routine", "Ejecutar rutina para clase 9")
        listener.get_logger().info("Sent routine command to Lite 6 for class 9")
    elif listener.detected_class == '8':
        # Ejecutar una rutina específica para la clase '8'
        listener.publish_mqtt("lite6/routine", "Ejecutar rutina para clase 8")
        listener.get_logger().info("Sent routine command to Lite 6 for class 8")
    else:
        # Rutina por defecto para otras clases
        listener.publish_mqtt("lite6/routine", f"Ejecutar rutina para clase {listener.detected_class}")
        listener.get_logger().info(f"Sent routine command to Lite 6 for class {listener.detected_class}")

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
        # Set goal pose
        goal_pose = navigator.getPoseStamped(GOAL_COORDINATE, TurtleBot4Directions.EAST)

        while rclpy.ok():
            if mqtt_listener.stop_flag:
                navigator.info('Stopping cycle due to stop flag')
                break

            if mqtt_listener.move_flag:
                # Mover al goal_pose
                navigator.info('Moving to goal_pose')
                navigator.startToPose(goal_pose)
                mqtt_listener.move_flag = False  
                mqtt_listener.get_logger().info("Robot started moving")

                result = navigator.getResult()

                if result == TaskResult.SUCCEEDED:
                    mqtt_listener.publish_mqtt("robot/arrival_status", "Arrived at goal_pose")
                    execute_lite6_routine(mqtt_listener)  # Ejecutar la rutina del Lite 6

                # Regresar al initial_pose
                navigator.info('Returning to initial_pose')
                initial_pose = navigator.getPoseStamped(INITIAL_COORDINATE, TurtleBot4Directions.NORTH)
                navigator.startToPose(initial_pose)
                
                if result == TaskResult.SUCCEEDED:
                    mqtt_listener.publish_mqtt("robot/arrival_status", "Arrived at initial_pose")

                mqtt_listener.get_logger().info("Robot completed the cycle")

            time.sleep(1)

    except Exception as e:
        navigator.error(f'An exception occurred: {e}')
    finally:
        mqtt_listener.stop() 
        mqtt_listener.client.loop_stop()
        mqtt_listener.client.disconnect()
        mqtt_listener.destroy_node()
        rclpy.shutdown()

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
        goal_pose = navigator.getPoseStamped(GOAL_COORDINATE, TurtleBot4Directions.EAST)

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

                if result == TaskResult.SUCCEEDED:
                    mqtt_listener.publish_mqtt("robot/arrival_status", "Arrived at goal_pose")
                    mqtt_listener.get_logger().info("Robot arrived at goal_pose")

                # Wait for MQTT signal for xArm to move
                if mqtt_listener.arm_move_flag:
                    mqtt_listener.get_logger().info("Starting xArm movement based on detected class")
                    mqtt_listener.move_arm()

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
                time.sleep(2)

            if position == [142.7, 56, 105.3, -0.1, 49.3, 85.2]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)
#J----------------------------------------------------------------
                
            if position == [45.6,14.4,99.5,-2.4,77.5,-24.1]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [142.3,41.5,81.2,2.8,39.8,84.4]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)
#Barra----------------------------------------------------------------

            if position == [34.6,24,112.3,0.8,75.6,-37.5]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [137.9, 33.2, 68.1, -0.2, 35.9, 85]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)
#Triangulo----------------------------------------------------------------
            
            if position == [71.6, 25.6, 114.8, -3.6, 77.7, -7.4]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [133.5,49.1,93.1,3.2,41.1,68.7]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)
#Y----------------------------------------------------------------
            
            if position == [60.2,35.8,129,0.6,80.8,-18.8]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [132,41.8,82,-9,34.5,77.5]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)

#PP----------------------------------------------------------------
            
            if position == [45,37.6,130,10.7,66.8,-32.8]:
                self.get_logger().info('Reached grip position, closing gripper')
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [136,53.9,100.3,-5.8,33.4,80.9]:
                self.get_logger().info('Reached place position, opening gripper')
                arm.open_lite6_gripper()
                time.sleep(2)
            time.sleep(2)  

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
def move_arm_for_class_8(self): #Digitos
        ip = '192.168.1.186'
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
            time.sleep(2)
            if position == [50.6, 22, 110.3, 1.6, 75.9, 16.7]:
                arm.close_lite6_gripper()
                time.sleep(2)

            if position == [147.9, 74, 138.5, 10.4, 48.3, 95.3]:
                arm.open_lite6_gripper()
                time.sleep(2)


        arm.open_lite6_gripper()
        arm.disconnect()

if __name__ == '__main__':
    main()