
import os
import sys
import time
import math
from xarm.wrapper import XArmAPI


ip = "192.168.2.186"
arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)



speed = 25

angles = [

            #Home
            [90,0,180,-90,-5,10],

            #1
            #pick
            [50,20,130,0,80,0],
            #packman grande
            [62.7,8,92.4,1.3,79.5,-8.7],
            #Gripper close
            #packman grande arriba
            [62.7,-5.8,92.4,-0.7,79.3,-9.6],
            #control arriba
            [128.1,6.8,107.3,3,74.5,5.8],
            #dejar packman grande 
            [142.7, 56, 105.3, -0.1, 49.3, 85.2],
            #open gripper
            #control arriba
            [128.1,6.8,107.3,3,74.5,5.8],

            #2
            #pick
            [50,20,130,0,80,0],
            #jota
            [45.6,14.4,99.5,-2.4,77.5,-24.1],
            #jota arriba
            [45.6,5.1,99.5,-3.3,74.6,-24.5],
            #control arriba
            [128.1,6.8,107.3,3,74.5,5.8],
            #dejar jota 
            [142.3,41.5,81.2,2.8,39.8,84.4],
            #open gripper
            #control arriba
            [128.1,6.8,107.3,3,74.5,5.8],

            #3
            #pick
            [50,20,130,0,80,0],
            #barra
            [34.6,24,112.3,0.8,75.6,-37.5],
            #barra arriba
            [34.6,23.1,117.6,-1.6,77.2,-35.4],
            #control arriba
            [128.1,6.8,107.3,3,74.5,5.8],
            #dejar barra
            [137.9, 33.2, 68.1, -0.2, 35.9, 85],
            #open gripper
            #control arriba
            [128.1,6.8,107.3,3,74.5,5.8],

            #4
            #pick
            [50,20,130,0,80,0],
            #triangulo
            [71.6, 25.6, 114.8, -3.6, 77.7, -7.4],
            #triangulo arriba
            [68.5,19.7,111.5,1.9,73.6,-8.4],
            #control arriba
            [128.1,6.8,107.3,3,74.5,5.8],
            #dejar triangulo
            [133.5,49.1,93.1,3.2,41.1,68.7],
            #open gripper
            #control arriba
            [128.1,6.8,107.3,3,74.5,5.8],



            #5
            #pick
            [50,20,130,0,80,0],
            #ye
            [60.2,35.8,129,0.6,80.8,-18.8],
            #ye arriba
            [60.1,32.1,129.2,-0.6,78.4,-18.6],
            #control arriba
            [128.1,6.8,107.3,3,74.5,5.8],
            #dejar ye
            [132,41.8,82,-9,34.5,77.5],
            #open gripper
            #control arriba
            [128.1,6.8,107.3,3,74.5,5.8],


            #6
            #pick
            [50,20,130,0,80,0],
            #packman chico
            [45,37.6,130,10.7,66.8,-32.8],
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
            [90,0,180,-90,-5,10],

            ###############################
            #Digitos
            #Home
            [90,0,180,-90,-5,10],

            #1
            #pick
            [50,20,130,0,80,0],
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


            ################################

            #Huevo
            #Home
            [90,0,180,-90,-5,10],

            #1
            #pick
            [50,20,130,0,80,0],
            #Huevo agarrar
            [49.1, 23.2, 115.1, 2.6, 77.6, -23.7],
            #Gripper close

            #Huevo arriba
            [49.1, 14.2, 115.1, 1.9, 77.6, -23.3],
            #control arriba
            [128.1,6.8,107.3,3,74.5,5.8],
            #Dejar huevo
            [124.7, 60, 115.1, 2.1, 41, -58.7]
            #Gripper open
            ]

arm.set_pause_time(1)

for angle in angles:
        code = arm.set_servo_angle(angle=angle, speed=speed, wait=True)

        if angle == [50,20,130,0,80,0]:          
                arm.open_lite6_gripper()
                time.sleep(1)  
#PG----------------------------------------------------------------
        if angle == [62.7,8,92.4,1.3,79.5,-8.7]:
                arm.close_lite6_gripper()
                time.sleep(2)

        if angle == [142.7, 56, 105.3, -0.1, 49.3, 85.2]:
                arm.open_lite6_gripper()
                time.sleep(2)

#J----------------------------------------------------------------
                
        if angle == [45.6,14.4,99.5,-2.4,77.5,-24.1]:
                arm.close_lite6_gripper()
                time.sleep(2)

        if angle == [142.3,41.5,81.2,2.8,39.8,84.4]:
                arm.open_lite6_gripper()
                time.sleep(2)
#Barra----------------------------------------------------------------

        if angle == [34.6,24,112.3,0.8,75.6,-37.5]:
                arm.close_lite6_gripper()
                time.sleep(2)

        if angle == [137.9, 33.2, 68.1, -0.2, 35.9, 85]:
                arm.open_lite6_gripper()
                time.sleep(2)
#Triangulo----------------------------------------------------------------
            
        if angle == [71.6, 25.6, 114.8, -3.6, 77.7, -7.4]:
                arm.close_lite6_gripper()
                time.sleep(2)

        if angle == [133.5,49.1,93.1,3.2,41.1,68.7]:
                arm.open_lite6_gripper()
                time.sleep(2)
#Y----------------------------------------------------------------
            
        if angle == [60.2,35.8,129,0.6,80.8,-18.8]:
                arm.close_lite6_gripper()
                time.sleep(2)

        if angle == [132,41.8,82,-9,34.5,77.5]:
                arm.open_lite6_gripper()
                time.sleep(2)

#PP----------------------------------------------------------------
            
        if angle == [45,37.6,130,10.7,66.8,-32.8]:
                arm.close_lite6_gripper()
                time.sleep(2)

        if angle == [136,53.9,100.3,-5.8,33.4,80.9]:
                arm.open_lite6_gripper()
                time.sleep(2)
        time.sleep(2)  

#DIGITOS----------------------------------------------------------------
            
        if angle == [50.6, 22, 110.3, 1.6, 75.9, 16.7]:
                arm.close_lite6_gripper()
                time.sleep(2)

        if angle == [147.9, 74, 138.5, 10.4, 48.3, 95.3]:
                arm.open_lite6_gripper()
                time.sleep(2)
        time.sleep(2)  

#HUEVO----------------------------------------------------------------
            
        if angle == [49.1, 23.2, 115.1, 2.6, 77.6, -23.7]:
                arm.close_lite6_gripper()
                time.sleep(2)

        if angle == [124.7, 60, 115.1, 2.1, 41, -58.7]:
                arm.open_lite6_gripper()
                time.sleep(2)
        time.sleep(2)  

time.sleep(2)
arm.disconnect()