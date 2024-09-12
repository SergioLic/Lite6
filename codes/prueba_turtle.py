import rclpy
from rclpy.node import Node
from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import paho.mqtt.client as mqtt
import re
import time

GOAL_COORDINATE = [-0.20,-0.83]
INITIAL_COORDINATE = [0.0, 0.0]

class MQTTListener(Node):
    def __init__(self, navigator):
        super().__init__('mqtt_listener')
        self.navigator = navigator
        self.move_flag = False  
        self.stop_flag = False  
        
        # Configuración del cliente MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # Conectar al broker MQTT
        #self.client.connect("10.50.40.49", 1883, 60)
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
            detected_class = match.group(1)
            self.get_logger().info(f'Detected class: {detected_class}')
            
            if detected_class == '9':
                self.get_logger().info('Detected class "9", starting movement cycle')
                self.move_flag = True  
                self.stop_flag = False

    def publish_mqtt(self, topic, message):
        # Publicar un mensaje en el broker MQTT
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

                #navigator.waitUntilNav2Arrived()  

                # Publicar que el robot llegó al goal_pose
                #mqtt_listener.publish_mqtt("robot/arrival_status", "Arrived at goal_pose")

                # Regresar al initial_pose
                navigator.info('Returning to initial_pose')
                initial_pose = navigator.getPoseStamped(INITIAL_COORDINATE, TurtleBot4Directions.NORTH)
                navigator.startToPose(initial_pose)
                
                if result == TaskResult.SUCCEEDED:
                     mqtt_listener.publish_mqtt("robot/arrival_status", "Arrived at initial_pose")
                #navigator.waitUntilArrived()

                # Publicar que el robot llegó al initial_pose
                #mqtt_listener.publish_mqtt("robot/arrival_status", "Arrived at initial_pose")

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

if __name__ == '__main__':
    main()


# import rclpy

# from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator


# def main():
#     rclpy.init()

#     navigator = TurtleBot4Navigator()

#     # Start on dock
#     if not navigator.getDockedStatus():
#         navigator.info('Docking before initialising pose')
#         navigator.dock()

#     # Set initial pose
#     initial_pose = navigator.getPoseStamped([0.0, 0.0], TurtleBot4Directions.NORTH)
#     navigator.setInitialPose(initial_pose)

#     # Wait for Nav2
#     navigator.waitUntilNav2Active()

#     # Set goal poses
#     goal_pose = navigator.getPoseStamped([-0.20,-0.83], TurtleBot4Directions.NORTH)

#     # Undock
#     navigator.undock()

#     # Go to each goal pose
#     navigator.startToPose(goal_pose)

#     rclpy.shutdown()
