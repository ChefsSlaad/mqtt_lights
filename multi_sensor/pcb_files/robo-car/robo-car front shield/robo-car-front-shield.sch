EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Wire Line
	1300 5450 1400 5450
Wire Wire Line
	1300 5550 1400 5550
Text Label 3450 5250 2    50   ~ 0
LINE_FOLLOW_L
Text Label 1400 5450 0    50   ~ 0
5V
Text Label 1400 5550 0    50   ~ 0
GND
$Comp
L Connector:Conn_01x03_Female J10
U 1 1 5EEFA3F1
P 2000 5450
F 0 "J10" H 2000 5950 50  0000 R CNN
F 1 "Line_follower_M" H 2000 5850 50  0000 R CNN
F 2 "robo-car:linefollower" H 2000 5450 50  0001 C CNN
F 3 "~" H 2000 5450 50  0001 C CNN
	1    2000 5450
	-1   0    0    -1  
$EndComp
Wire Wire Line
	2200 5450 2300 5450
Wire Wire Line
	2200 5550 2300 5550
Text Label 2600 5250 2    50   ~ 0
LINE_FOLLOW_M
Text Label 2300 5450 0    50   ~ 0
5V
Text Label 2300 5550 0    50   ~ 0
GND
$Comp
L Connector:Conn_01x03_Female J11
U 1 1 5EEFBFF0
P 2900 5450
F 0 "J11" H 2900 5950 50  0000 R CNN
F 1 "Line_follower_L" H 2900 5850 50  0000 R CNN
F 2 "robo-car:linefollower" H 2900 5450 50  0001 C CNN
F 3 "~" H 2900 5450 50  0001 C CNN
	1    2900 5450
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3100 5450 3200 5450
Wire Wire Line
	3100 5550 3200 5550
Text Label 1650 5250 2    50   ~ 0
LINE_FOLLOW_R
Text Label 3200 5450 0    50   ~ 0
5V
Text Label 3200 5550 0    50   ~ 0
GND
$Comp
L Connector:Conn_01x04_Female J12
U 1 1 5EF124AE
P 3850 5600
F 0 "J12" H 3850 5950 50  0000 R CNN
F 1 "HC-SR04" H 3850 5850 50  0000 R CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Vertical" H 3850 5600 50  0001 C CNN
F 3 "~" H 3850 5600 50  0001 C CNN
	1    3850 5600
	-1   0    0    1   
$EndComp
Wire Wire Line
	4050 5700 4150 5700
Wire Wire Line
	4050 5400 4150 5400
Text Label 4150 5700 0    50   ~ 0
GND
Text Label 4150 5400 0    50   ~ 0
5V
Text Label 4150 5600 0    50   ~ 0
ECHO_FRONT
Text Label 4150 5500 0    50   ~ 0
TRIG_FRONT
$Comp
L Connector:Conn_01x03_Female J9
U 1 1 5EEED897
P 1100 5450
F 0 "J9" H 1100 5950 50  0000 R CNN
F 1 "Line_follower_R" H 1150 5850 50  0000 R CNN
F 2 "robo-car:linefollower" H 1100 5450 50  0001 C CNN
F 3 "~" H 1100 5450 50  0001 C CNN
	1    1100 5450
	-1   0    0    -1  
$EndComp
$Comp
L Device:R_Small R2
U 1 1 5EEFF93B
P 1550 5350
F 0 "R2" V 1550 5350 50  0000 C CNN
F 1 "330R" V 1550 5550 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" H 1550 5350 50  0001 C CNN
F 3 "~" H 1550 5350 50  0001 C CNN
	1    1550 5350
	0    1    1    0   
$EndComp
Wire Wire Line
	1300 5350 1450 5350
Wire Wire Line
	2200 5350 2400 5350
Wire Wire Line
	3100 5350 3250 5350
Wire Wire Line
	3450 5350 3450 5250
$Comp
L Device:R_Small R3
U 1 1 5EF4C370
P 2500 5350
F 0 "R3" V 2500 5350 50  0000 C CNN
F 1 "330R" V 2500 5550 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" H 2500 5350 50  0001 C CNN
F 3 "~" H 2500 5350 50  0001 C CNN
	1    2500 5350
	0    1    1    0   
$EndComp
$Comp
L Device:R_Small R4
U 1 1 5EF4CF38
P 3350 5350
F 0 "R4" V 3350 5350 50  0000 C CNN
F 1 "330R" V 3350 5550 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" H 3350 5350 50  0001 C CNN
F 3 "~" H 3350 5350 50  0001 C CNN
	1    3350 5350
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x07_Male J19
U 1 1 5F011F63
P 5250 5400
F 0 "J19" H 5150 5450 50  0000 R CNN
F 1 "front_connect" H 5150 5550 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x07_P2.54mm_Vertical" H 5250 5400 50  0001 C CNN
F 3 "~" H 5250 5400 50  0001 C CNN
	1    5250 5400
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5050 5700 4950 5700
Wire Wire Line
	5050 5100 4950 5100
Text Label 4950 5700 2    50   ~ 0
5V
Text Label 4950 5100 2    50   ~ 0
GND
Wire Wire Line
	4050 5600 4550 5600
Wire Wire Line
	3450 5250 4650 5250
Wire Wire Line
	4650 5250 4650 5400
Wire Wire Line
	4650 5400 5050 5400
Wire Wire Line
	2600 5200 4700 5200
Wire Wire Line
	4700 5200 4700 5300
Wire Wire Line
	4700 5300 5050 5300
Wire Wire Line
	2600 5200 2600 5350
Wire Wire Line
	1650 5150 4750 5150
Wire Wire Line
	4750 5150 4750 5200
Wire Wire Line
	4750 5200 5050 5200
Wire Wire Line
	1650 5150 1650 5350
Wire Wire Line
	4600 5500 4600 5450
Wire Wire Line
	4550 5600 4550 5550
Wire Wire Line
	4600 5500 5050 5500
Wire Wire Line
	4050 5500 4600 5500
Connection ~ 4550 5600
Connection ~ 4600 5500
Wire Wire Line
	4550 5600 5050 5600
$Comp
L power:PWR_FLAG #FLG02
U 1 1 5EFE9BBF
P 5050 5700
F 0 "#FLG02" H 5050 5775 50  0001 C CNN
F 1 "PWR_FLAG" H 5050 5873 50  0000 C CNN
F 2 "" H 5050 5700 50  0001 C CNN
F 3 "~" H 5050 5700 50  0001 C CNN
	1    5050 5700
	-1   0    0    1   
$EndComp
Connection ~ 5050 5700
$Comp
L power:PWR_FLAG #FLG01
U 1 1 5EFE9E21
P 5050 5100
F 0 "#FLG01" H 5050 5175 50  0001 C CNN
F 1 "PWR_FLAG" H 5050 5273 50  0000 C CNN
F 2 "" H 5050 5100 50  0001 C CNN
F 3 "~" H 5050 5100 50  0001 C CNN
	1    5050 5100
	1    0    0    -1  
$EndComp
Connection ~ 5050 5100
$EndSCHEMATC
