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
$Comp
L Connector:Screw_Terminal_01x02 J18
U 1 1 5EEA43B7
P 1000 6850
F 0 "J18" V 1150 6800 50  0000 C CNN
F 1 "battery screw terminal" V 1100 6800 50  0000 C CNN
F 2 "TerminalBlock:TerminalBlock_Altech_AK300-2_P5.00mm" H 1000 6850 50  0001 C CNN
F 3 "~" H 1000 6850 50  0001 C CNN
	1    1000 6850
	0    1    -1   0   
$EndComp
$Comp
L robocar_custom:LM2596-custom P1
U 1 1 5EEA5CF4
P 2550 7200
F 0 "P1" H 2575 7525 50  0000 C CNN
F 1 "LM2596-custom" H 2575 7434 50  0000 C CNN
F 2 "robo-car:lm2596-custom" H 2550 7200 50  0001 C CNN
F 3 "" H 2550 7200 50  0001 C CNN
	1    2550 7200
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 7150 2150 7100
Wire Wire Line
	2150 7250 2150 7300
$Comp
L power:+7.5V #PWR01
U 1 1 5EEA7F10
P 1800 7150
F 0 "#PWR01" H 1800 7000 50  0001 C CNN
F 1 "+7.5V" V 1800 7400 50  0000 C CNN
F 2 "" H 1800 7150 50  0001 C CNN
F 3 "" H 1800 7150 50  0001 C CNN
	1    1800 7150
	1    0    0    -1  
$EndComp
Text Label 3650 7050 0    50   ~ 0
5V
Text Label 3650 7350 0    50   ~ 0
GND
Wire Wire Line
	2050 1000 2050 900 
Wire Wire Line
	2050 900  2100 900 
Wire Wire Line
	2150 900  2150 1000
Wire Wire Line
	2100 900  2100 850 
Connection ~ 2100 900 
Wire Wire Line
	2100 900  2150 900 
Text Label 2100 850  0    50   ~ 0
5V
Wire Wire Line
	1850 3750 1850 3650
Text Label 1850 3750 0    50   ~ 0
GND
Wire Wire Line
	1850 3650 1950 3650
Wire Wire Line
	1950 3650 1950 3600
Connection ~ 1850 3650
Wire Wire Line
	1850 3650 1850 3600
Wire Wire Line
	1950 3650 2050 3650
Wire Wire Line
	2050 3650 2050 3600
Connection ~ 1950 3650
Wire Wire Line
	2050 3650 2150 3650
Wire Wire Line
	2150 3650 2150 3600
Connection ~ 2050 3650
Wire Wire Line
	2150 3650 2250 3650
Wire Wire Line
	2250 3650 2250 3600
Connection ~ 2150 3650
Wire Wire Line
	2250 3650 2350 3650
Wire Wire Line
	2350 3650 2350 3600
Connection ~ 2250 3650
Wire Wire Line
	2350 3650 2450 3650
Wire Wire Line
	2450 3650 2450 3600
Connection ~ 2350 3650
Wire Wire Line
	2450 3650 2550 3650
Wire Wire Line
	2550 3650 2550 3600
Connection ~ 2450 3650
$Comp
L Connector:Conn_01x03_Male J6
U 1 1 5EEBAD2C
P 1150 4400
F 0 "J6" H 1258 4681 50  0000 C CNN
F 1 "SERVO1" H 1258 4590 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 1150 4400 50  0001 C CNN
F 3 "~" H 1150 4400 50  0001 C CNN
	1    1150 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	1350 4300 1500 4300
Wire Wire Line
	1350 4400 1500 4400
Wire Wire Line
	1350 4500 1500 4500
Text Label 1500 4300 0    50   ~ 0
GND
Text Label 1500 4400 0    50   ~ 0
5V
Text Label 1500 4500 0    50   ~ 0
SERVO1
Wire Wire Line
	2250 4300 2400 4300
Wire Wire Line
	2250 4400 2400 4400
Wire Wire Line
	2250 4500 2400 4500
Text Label 2400 4300 0    50   ~ 0
GND
Text Label 2400 4400 0    50   ~ 0
5V
Text Label 2400 4500 0    50   ~ 0
SERVO2
Wire Wire Line
	1450 1500 1300 1500
Wire Wire Line
	1450 1700 1300 1700
Wire Wire Line
	1450 1800 1300 1800
Wire Wire Line
	1450 1900 1300 1900
Wire Wire Line
	1450 2100 1300 2100
Wire Wire Line
	1450 2200 1300 2200
Wire Wire Line
	1450 2300 1300 2300
Wire Wire Line
	1450 2500 1300 2500
Wire Wire Line
	1450 2600 1300 2600
Wire Wire Line
	1450 2700 1300 2700
Wire Wire Line
	1450 2800 1300 2800
Wire Wire Line
	1450 2900 1300 2900
Wire Wire Line
	1450 3000 1300 3000
Wire Wire Line
	3050 1700 3200 1700
Wire Wire Line
	1450 1400 1300 1400
Wire Wire Line
	3050 2000 3200 2000
Wire Wire Line
	3050 2700 3200 2700
Wire Wire Line
	3050 2800 3200 2800
Wire Wire Line
	3050 3100 3200 3100
Wire Wire Line
	3050 1800 3200 1800
Wire Wire Line
	3050 3000 3200 3000
Text Label 3200 2800 0    50   ~ 0
SERVO1
Text Label 1300 2800 2    50   ~ 0
SERVO2
Text Label 3200 3100 0    50   ~ 0
LINE_FOLLOW_L
Text Label 3200 2200 0    50   ~ 0
LINE_FOLLOW_M
Text Label 3200 2100 0    50   ~ 0
LINE_FOLLOW_R
Wire Wire Line
	3150 4500 3250 4500
Wire Wire Line
	3150 4400 3250 4400
Wire Wire Line
	3150 4300 3250 4300
Text Label 3250 4300 0    50   ~ 0
GND
Text Label 3250 4400 0    50   ~ 0
ECHO_CAM
Text Label 3250 4500 0    50   ~ 0
TRIG_CAM
Text Label 3250 4600 0    50   ~ 0
5V
Wire Wire Line
	3150 4600 3250 4600
$Comp
L Connector:Conn_01x03_Male J7
U 1 1 5EEC2EEE
P 2050 4400
F 0 "J7" H 2100 4750 50  0000 C CNN
F 1 "SERVO2" H 2200 4650 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 2050 4400 50  0001 C CNN
F 3 "~" H 2050 4400 50  0001 C CNN
	1    2050 4400
	1    0    0    -1  
$EndComp
Text Label 3200 2700 0    50   ~ 0
ECHO_CAM
Text Label 3200 2600 0    50   ~ 0
TRIG_CAM
Text Label 1300 2100 2    50   ~ 0
ECHO_FRONT
Text Label 1300 1700 2    50   ~ 0
TRIG_FRONT
$Comp
L Sensor_Temperature:DS18B20 U10
U 1 1 5EFB1D29
P 1300 6150
F 0 "U10" V 933 6150 50  0000 C CNN
F 1 "DS18B20" V 1024 6150 50  0000 C CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 300 5900 50  0001 C CNN
F 3 "http://datasheets.maximintegrated.com/en/ds/DS18B20.pdf" H 1150 6400 50  0001 C CNN
	1    1300 6150
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x03_Female J13
U 1 1 5EFB3837
P 2050 6100
F 0 "J13" H 1950 6450 50  0000 C CNN
F 1 "DHT11" H 1950 6350 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x03_P2.54mm_Vertical" H 2050 6100 50  0001 C CNN
F 3 "~" H 2050 6100 50  0001 C CNN
	1    2050 6100
	-1   0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 5EFBF0F6
P 1500 6450
F 0 "R1" V 1700 6450 50  0000 C CNN
F 1 "4K7" V 1600 6450 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 1430 6450 50  0001 C CNN
F 3 "~" H 1500 6450 50  0001 C CNN
	1    1500 6450
	0    1    1    0   
$EndComp
Text Label 1750 6150 0    50   ~ 0
5V
Wire Wire Line
	1600 6150 1650 6150
Wire Wire Line
	1650 6450 1650 6150
Connection ~ 1650 6150
Wire Wire Line
	1650 6150 1750 6150
Wire Wire Line
	1300 6450 1350 6450
Wire Wire Line
	1300 6450 1300 6550
Connection ~ 1300 6450
Text Label 1000 6150 2    50   ~ 0
GND
Text Label 1300 6550 2    50   ~ 0
TEMP
Wire Wire Line
	2250 6000 2350 6000
Wire Wire Line
	2250 6100 2350 6100
Wire Wire Line
	2250 6200 2350 6200
Text Label 2350 6000 0    50   ~ 0
HUMIDITY
Text Label 2350 6100 0    50   ~ 0
5V
Text Label 2350 6200 0    50   ~ 0
GND
$Comp
L Connector:Conn_01x05_Female J14
U 1 1 5EFDE53F
P 2850 6150
F 0 "J14" H 2800 6550 50  0000 C CNN
F 1 "RCWL-0516" H 2650 6450 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical" H 2850 6150 50  0001 C CNN
F 3 "~" H 2850 6150 50  0001 C CNN
	1    2850 6150
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3050 5950 3200 5950
Wire Wire Line
	3050 6050 3200 6050
Wire Wire Line
	3050 6150 3200 6150
Wire Wire Line
	3050 6250 3200 6250
Wire Wire Line
	3050 6350 3200 6350
NoConn ~ 3200 6350
NoConn ~ 3200 5950
Text Label 3200 6050 0    50   ~ 0
GND
Text Label 3200 6150 0    50   ~ 0
MOTION
Text Label 3200 6250 0    50   ~ 0
5V
$Comp
L Driver_Motor:L293D U1
U 1 1 5F000CA1
P 6350 1950
F 0 "U1" H 6350 3200 50  0000 C CNN
F 1 "L293D" H 6350 3100 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 6600 1200 50  0001 L CNN
F 3 "http://www.ti.com/lit/ds/symlink/l293.pdf" H 6050 2650 50  0001 C CNN
	1    6350 1950
	1    0    0    -1  
$EndComp
Wire Wire Line
	6150 2750 6150 2800
Wire Wire Line
	6550 2750 6550 2800
Wire Wire Line
	6550 2800 6450 2800
Connection ~ 6150 2800
Wire Wire Line
	6150 2800 6150 2900
Wire Wire Line
	6450 2800 6450 2750
Connection ~ 6450 2800
Wire Wire Line
	6450 2800 6250 2800
Wire Wire Line
	6250 2750 6250 2800
Connection ~ 6250 2800
Wire Wire Line
	6250 2800 6150 2800
Wire Wire Line
	6450 950  6450 850 
Wire Wire Line
	6450 850  6550 850 
Text Label 6550 850  0    50   ~ 0
7V5
Text Label 5700 850  2    50   ~ 0
5V
Text Label 6950 2050 0    50   ~ 0
MOTOR1+
Text Label 6950 1950 0    50   ~ 0
MOTOR1-
Text Label 6950 1350 0    50   ~ 0
MOTOR2+
Text Label 6950 1450 0    50   ~ 0
MOTOR2-
Text Label 5800 1350 2    50   ~ 0
MOTOR1_F
Text Label 5800 1550 2    50   ~ 0
MOTOR1_B
Text Label 5800 1950 2    50   ~ 0
MOTOR2_F
Text Label 5800 2150 2    50   ~ 0
MOTOR2_B
$Comp
L Connector:Screw_Terminal_01x02 J1
U 1 1 5F0337F0
P 7550 2050
F 0 "J1" H 7630 2042 50  0000 L CNN
F 1 "MOTOR1" H 7630 1951 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_Altech_AK300-2_P5.00mm" H 7550 2050 50  0001 C CNN
F 3 "~" H 7550 2050 50  0001 C CNN
	1    7550 2050
	1    0    0    1   
$EndComp
$Comp
L Connector:Screw_Terminal_01x02 J2
U 1 1 5F034067
P 7550 1350
F 0 "J2" H 7630 1342 50  0000 L CNN
F 1 "MOTOR2" H 7630 1251 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_Altech_AK300-2_P5.00mm" H 7550 1350 50  0001 C CNN
F 3 "~" H 7550 1350 50  0001 C CNN
	1    7550 1350
	1    0    0    -1  
$EndComp
Wire Wire Line
	6250 950  5700 950 
Wire Wire Line
	5400 950  5400 1750
Wire Wire Line
	5400 1750 5850 1750
Wire Wire Line
	5400 1750 5400 2350
Wire Wire Line
	5400 2350 5850 2350
Connection ~ 5400 1750
Wire Wire Line
	5700 850  5700 950 
Connection ~ 5700 950 
Wire Wire Line
	5700 950  5400 950 
Text Label 6150 2900 0    50   ~ 0
GND
Wire Wire Line
	9100 2750 9100 2800
Wire Wire Line
	9500 2750 9500 2800
Wire Wire Line
	9500 2800 9400 2800
Connection ~ 9100 2800
Wire Wire Line
	9100 2800 9100 2900
Wire Wire Line
	9400 2800 9400 2750
Connection ~ 9400 2800
Wire Wire Line
	9400 2800 9200 2800
Wire Wire Line
	9200 2750 9200 2800
Connection ~ 9200 2800
Wire Wire Line
	9200 2800 9100 2800
Wire Wire Line
	9400 950  9400 850 
Wire Wire Line
	9400 850  9500 850 
Text Label 9500 850  0    50   ~ 0
7V5
Text Label 8650 850  2    50   ~ 0
5V
Text Label 9950 2050 0    50   ~ 0
MOTOR3+
Text Label 9950 1950 0    50   ~ 0
MOTOR3-
Text Label 9950 1350 0    50   ~ 0
MOTOR4+
Text Label 9950 1450 0    50   ~ 0
MOTOR4-
Text Label 8750 1350 2    50   ~ 0
MOTOR3_F
Text Label 8750 1550 2    50   ~ 0
MOTOR3_B
Text Label 8750 1950 2    50   ~ 0
MOTOR4_F
Text Label 8750 2150 2    50   ~ 0
MOTOR4_B
$Comp
L Connector:Screw_Terminal_01x02 J3
U 1 1 5F067516
P 10500 2050
F 0 "J3" H 10580 2042 50  0000 L CNN
F 1 "MOTOR3" H 10580 1951 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_Altech_AK300-2_P5.00mm" H 10500 2050 50  0001 C CNN
F 3 "~" H 10500 2050 50  0001 C CNN
	1    10500 2050
	1    0    0    1   
$EndComp
$Comp
L Connector:Screw_Terminal_01x02 J4
U 1 1 5F06751C
P 10500 1350
F 0 "J4" H 10580 1342 50  0000 L CNN
F 1 "MOTOR4" H 10580 1251 50  0000 L CNN
F 2 "TerminalBlock:TerminalBlock_Altech_AK300-2_P5.00mm" H 10500 1350 50  0001 C CNN
F 3 "~" H 10500 1350 50  0001 C CNN
	1    10500 1350
	1    0    0    -1  
$EndComp
Wire Wire Line
	9200 950  8650 950 
Wire Wire Line
	8350 950  8350 1750
Wire Wire Line
	8350 1750 8800 1750
Wire Wire Line
	8350 1750 8350 2350
Wire Wire Line
	8350 2350 8800 2350
Connection ~ 8350 1750
Wire Wire Line
	8650 850  8650 950 
Connection ~ 8650 950 
Wire Wire Line
	8650 950  8350 950 
Text Label 9100 2900 0    50   ~ 0
GND
$Comp
L Device:CP CP1
U 1 1 5F0973CB
P 3200 7200
F 0 "CP1" H 3318 7246 50  0000 L CNN
F 1 "100uF" H 3318 7155 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 3238 7050 50  0001 C CNN
F 3 "~" H 3200 7200 50  0001 C CNN
	1    3200 7200
	1    0    0    -1  
$EndComp
$Comp
L Device:CP CP2
U 1 1 5F098BCD
P 3600 7200
F 0 "CP2" H 3718 7246 50  0000 L CNN
F 1 "4.7uF" H 3718 7155 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D4.0mm_P2.00mm" H 3638 7050 50  0001 C CNN
F 3 "~" H 3600 7200 50  0001 C CNN
	1    3600 7200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 7050 3000 7050
Wire Wire Line
	3000 7050 3000 7100
Wire Wire Line
	3000 7300 3000 7350
$Comp
L robocar_custom:WS2812B U3
U 1 1 5F0D7CA5
P 6850 3550
F 0 "U3" H 6850 3775 50  0000 C CNN
F 1 "WS2812B" H 6850 3684 50  0000 C CNN
F 2 "robo-car:neopixel_pcb" H 6750 3550 50  0001 C CNN
F 3 "" H 6750 3550 50  0001 C CNN
	1    6850 3550
	1    0    0    -1  
$EndComp
$Comp
L robocar_custom:WS2812B U4
U 1 1 5F0DF40D
P 7500 3550
F 0 "U4" H 7500 3775 50  0000 C CNN
F 1 "WS2812B" H 7500 3684 50  0000 C CNN
F 2 "robo-car:neopixel_pcb" H 7400 3550 50  0001 C CNN
F 3 "" H 7400 3550 50  0001 C CNN
	1    7500 3550
	1    0    0    -1  
$EndComp
$Comp
L robocar_custom:WS2812B U5
U 1 1 5F0E56F3
P 8150 3550
F 0 "U5" H 8150 3775 50  0000 C CNN
F 1 "WS2812B" H 8150 3684 50  0000 C CNN
F 2 "robo-car:neopixel_pcb" H 8050 3550 50  0001 C CNN
F 3 "" H 8050 3550 50  0001 C CNN
	1    8150 3550
	1    0    0    -1  
$EndComp
$Comp
L robocar_custom:WS2812B U6
U 1 1 5F0EBA4D
P 8800 3550
F 0 "U6" H 8800 3775 50  0000 C CNN
F 1 "WS2812B" H 8800 3684 50  0000 C CNN
F 2 "robo-car:neopixel_pcb" H 8700 3550 50  0001 C CNN
F 3 "" H 8700 3550 50  0001 C CNN
	1    8800 3550
	1    0    0    -1  
$EndComp
$Comp
L Device:CP CP3
U 1 1 5F13C0A7
P 5900 3650
F 0 "CP3" H 5600 3700 50  0000 L CNN
F 1 "470uF" H 5550 3600 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 5938 3500 50  0001 C CNN
F 3 "~" H 5900 3650 50  0001 C CNN
	1    5900 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	6550 3550 6550 3500
Wire Wire Line
	6550 3750 6550 3800
Text Label 6500 3650 2    50   ~ 0
NEOPIXEL
Wire Wire Line
	5900 3800 5750 3800
Connection ~ 5900 3800
Wire Wire Line
	5900 3500 5750 3500
Connection ~ 5900 3500
Text Label 5750 3500 2    50   ~ 0
5V
Text Label 5750 3800 2    50   ~ 0
GND
Wire Wire Line
	7150 3550 7200 3550
Wire Wire Line
	7200 3650 7150 3650
Wire Wire Line
	7150 3750 7200 3750
Wire Wire Line
	7800 3550 7850 3550
Wire Wire Line
	7800 3650 7850 3650
Wire Wire Line
	7800 3750 7850 3750
Wire Wire Line
	8450 3550 8500 3550
Wire Wire Line
	8450 3650 8500 3650
Wire Wire Line
	8450 3750 8500 3750
Wire Wire Line
	8800 1350 8750 1350
Wire Wire Line
	8800 1550 8750 1550
Wire Wire Line
	8800 1950 8750 1950
Wire Wire Line
	8800 2150 8750 2150
Wire Wire Line
	6500 3650 6550 3650
Wire Wire Line
	5800 1350 5850 1350
Wire Wire Line
	5850 1550 5800 1550
Wire Wire Line
	5850 1950 5800 1950
Wire Wire Line
	5850 2150 5800 2150
Text Label 1300 1900 2    50   ~ 0
MOTOR1_F
Text Label 1300 1500 2    50   ~ 0
MOTOR1_B
Text Label 1300 3000 2    50   ~ 0
MOTOR2_F
Text Label 1300 1800 2    50   ~ 0
MOTOR2_B
Text Label 3200 1800 0    50   ~ 0
MOTOR3_F
Text Label 3200 1700 0    50   ~ 0
MOTOR3_B
Text Label 3200 2000 0    50   ~ 0
MOTOR4_B
Text Label 1300 2700 2    50   ~ 0
TEMP
Text Label 1300 2500 2    50   ~ 0
MOTION
Text Label 1300 2600 2    50   ~ 0
HUMIDITY
$Comp
L Connector:Raspberry_Pi_2_3 J5
U 1 1 5EE9C8A7
P 2250 2300
F 0 "J5" H 2250 4050 50  0000 C CNN
F 1 "Raspberry_Pi_2_3" H 2250 3950 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical" H 2250 2300 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 2250 2300 50  0001 C CNN
	1    2250 2300
	1    0    0    -1  
$EndComp
NoConn ~ 2450 1000
NoConn ~ 2350 1000
Text Label 1950 7150 0    50   ~ 0
7V5
Text Label 1950 7250 0    50   ~ 0
GND
$Comp
L power:PWR_FLAG #FLG01
U 1 1 5F30D85B
P 1900 7150
F 0 "#FLG01" H 1900 7225 50  0001 C CNN
F 1 "PWR_FLAG" V 1900 7450 50  0000 C CNN
F 2 "" H 1900 7150 50  0001 C CNN
F 3 "~" H 1900 7150 50  0001 C CNN
	1    1900 7150
	1    0    0    -1  
$EndComp
Connection ~ 1900 7150
Wire Wire Line
	1900 7150 2150 7150
Wire Wire Line
	1800 7150 1900 7150
Text Label 3200 2400 0    50   ~ 0
GPIO07
Text Label 3200 3000 0    50   ~ 0
GPIO12
Text Label 3200 2500 0    50   ~ 0
GPIO08
Wire Wire Line
	3050 2600 3200 2600
$Comp
L power:GNDREF #PWR02
U 1 1 5EFA6953
P 1900 7250
F 0 "#PWR02" H 1900 7000 50  0001 C CNN
F 1 "GNDREF" H 1905 7077 50  0000 C CNN
F 2 "" H 1900 7250 50  0001 C CNN
F 3 "" H 1900 7250 50  0001 C CNN
	1    1900 7250
	1    0    0    -1  
$EndComp
Connection ~ 1900 7250
Wire Wire Line
	1900 7250 2150 7250
$Comp
L Device:Polyfuse F2
U 1 1 5EED3F26
P 3200 6850
F 0 "F2" H 3112 6804 50  0000 R CNN
F 1 "2A PolyFuse" H 3100 6850 50  0000 R CNN
F 2 "robo-car:restoring polyfuse" H 3250 6650 50  0001 L CNN
F 3 "~" H 3200 6850 50  0001 C CNN
	1    3200 6850
	-1   0    0    1   
$EndComp
$Comp
L Device:Fuse F1
U 1 1 5EEEA783
P 3100 6850
F 0 "F1" H 2950 6900 50  0000 L CNN
F 1 "2A Slow Blow" H 2700 7100 50  0000 L CNN
F 2 "robo-car:slow_blow_polyfuse" V 3030 6850 50  0001 C CNN
F 3 "~" H 3100 6850 50  0001 C CNN
	1    3100 6850
	1    0    0    -1  
$EndComp
Connection ~ 3200 7350
Connection ~ 3600 7050
Wire Wire Line
	3600 7050 3650 7050
Connection ~ 3600 7350
Wire Wire Line
	3600 7350 3650 7350
Wire Wire Line
	3000 7350 3200 7350
Wire Wire Line
	3200 7350 3600 7350
Wire Wire Line
	3200 7000 3200 7050
Wire Wire Line
	3200 7050 3600 7050
Connection ~ 3200 7050
Wire Wire Line
	3100 7050 3100 7000
Wire Wire Line
	3100 6700 3200 6700
$Comp
L Switch:SW_SPDT SW1
U 1 1 5EF27DE0
P 1450 7050
F 0 "SW1" H 1300 7250 50  0000 C CNN
F 1 "SW_SPDT" H 1300 7150 50  0000 C CNN
F 2 "robo-car:rocker switch 8.5x3.5mm 2.54piych" H 1450 7050 50  0001 C CNN
F 3 "~" H 1450 7050 50  0001 C CNN
	1    1450 7050
	1    0    0    -1  
$EndComp
Wire Wire Line
	1650 7150 1800 7150
Connection ~ 1800 7150
Wire Wire Line
	1250 7050 1000 7050
Wire Wire Line
	900  7050 900  7250
Wire Wire Line
	900  7250 1900 7250
$Comp
L Driver_Motor:L293D U2
U 1 1 5F0674F9
P 9300 1950
F 0 "U2" H 9300 3200 50  0000 C CNN
F 1 "L293D" H 9300 3100 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 9550 1200 50  0001 L CNN
F 3 "http://www.ti.com/lit/ds/symlink/l293.pdf" H 9000 2650 50  0001 C CNN
	1    9300 1950
	1    0    0    -1  
$EndComp
Wire Wire Line
	9800 1350 10300 1350
Wire Wire Line
	9800 1550 9950 1550
Wire Wire Line
	9950 1550 9950 1450
Wire Wire Line
	10300 1450 9950 1450
Wire Wire Line
	9950 2150 9950 2050
Wire Wire Line
	10300 2050 9950 2050
Wire Wire Line
	9800 1950 10300 1950
Wire Wire Line
	9950 2150 9800 2150
Wire Wire Line
	6850 1550 6950 1550
Wire Wire Line
	6950 1550 6950 1450
Wire Wire Line
	7350 1450 6950 1450
Wire Wire Line
	6850 1350 7350 1350
Wire Wire Line
	6850 1950 7350 1950
Wire Wire Line
	6850 2150 6950 2150
Wire Wire Line
	6950 2150 6950 2050
Wire Wire Line
	7350 2050 6950 2050
Text Label 1300 1400 2    50   ~ 0
MOTOR4_F
Wire Wire Line
	3050 2100 3200 2100
Wire Wire Line
	3200 2200 3050 2200
Wire Wire Line
	3050 2400 3200 2400
Wire Wire Line
	3200 2500 3050 2500
Text Label 1300 2200 2    50   ~ 0
neopixel_left
Text Label 1300 2300 2    50   ~ 0
NEOPIXEL
Wire Wire Line
	5900 3500 6450 3500
Wire Wire Line
	7200 3550 7200 3250
Wire Wire Line
	7200 3250 6450 3250
Wire Wire Line
	6450 3250 6450 3500
Connection ~ 7200 3550
Connection ~ 6450 3500
Wire Wire Line
	6450 3500 6550 3500
Wire Wire Line
	7200 3250 7850 3250
Wire Wire Line
	7850 3250 7850 3550
Connection ~ 7200 3250
Connection ~ 7850 3550
Wire Wire Line
	7850 3250 8500 3250
Wire Wire Line
	8500 3250 8500 3550
Connection ~ 7850 3250
Connection ~ 8500 3550
Wire Wire Line
	7200 3950 7200 3750
Connection ~ 6450 3800
Connection ~ 7200 3750
Wire Wire Line
	7200 3950 7850 3950
Wire Wire Line
	7850 3950 7850 3750
Connection ~ 7200 3950
Connection ~ 7850 3750
Wire Wire Line
	6450 3800 6550 3800
Wire Wire Line
	5900 3800 6450 3800
Connection ~ 8500 3750
Wire Wire Line
	7850 3950 8500 3950
Connection ~ 7850 3950
Wire Wire Line
	6450 3800 6450 3950
Wire Wire Line
	6450 3950 7200 3950
NoConn ~ 3050 1400
NoConn ~ 3050 1500
$Comp
L Connector:Conn_01x07_Male J20
U 1 1 5F01764F
P 5500 5400
F 0 "J20" H 5650 6000 50  0000 R CNN
F 1 "front_connect" H 6100 5850 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x07_P2.54mm_Vertical" H 5500 5400 50  0001 C CNN
F 3 "~" H 5500 5400 50  0001 C CNN
	1    5500 5400
	1    0    0    -1  
$EndComp
Wire Wire Line
	5700 5600 5750 5600
Wire Wire Line
	5700 5500 5750 5500
Wire Wire Line
	5700 5400 5750 5400
Wire Wire Line
	5700 5300 5750 5300
Wire Wire Line
	5700 5200 5750 5200
Wire Wire Line
	5700 5100 5750 5100
Text Label 5750 5100 0    50   ~ 0
GND
Wire Wire Line
	5700 5700 5750 5700
Text Label 5750 5700 0    50   ~ 0
5V
Text Label 5750 5500 0    50   ~ 0
TRIG_FRONT
Text Label 5750 5600 0    50   ~ 0
ECHO_FRONT
Text Label 5750 5200 0    50   ~ 0
LINE_FOLLOW_R
Text Label 5750 5300 0    50   ~ 0
LINE_FOLLOW_M
Text Label 5750 5400 0    50   ~ 0
LINE_FOLLOW_L
$Comp
L robocar_custom:WS2812B U7
U 1 1 5F26293E
P 9500 3550
F 0 "U7" H 9500 3775 50  0000 C CNN
F 1 "WS2812B" H 9500 3684 50  0000 C CNN
F 2 "robo-car:neopixel_pcb" H 9400 3550 50  0001 C CNN
F 3 "" H 9400 3550 50  0001 C CNN
	1    9500 3550
	1    0    0    -1  
$EndComp
$Comp
L robocar_custom:WS2812B U8
U 1 1 5F262944
P 10150 3550
F 0 "U8" H 10150 3775 50  0000 C CNN
F 1 "WS2812B" H 10150 3684 50  0000 C CNN
F 2 "robo-car:neopixel_pcb" H 10050 3550 50  0001 C CNN
F 3 "" H 10050 3550 50  0001 C CNN
	1    10150 3550
	1    0    0    -1  
$EndComp
$Comp
L robocar_custom:WS2812B U9
U 1 1 5F26294A
P 10800 3550
F 0 "U9" H 10800 3775 50  0000 C CNN
F 1 "WS2812B" H 10800 3684 50  0000 C CNN
F 2 "robo-car:neopixel_pcb" H 10700 3550 50  0001 C CNN
F 3 "" H 10700 3550 50  0001 C CNN
	1    10800 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	9800 3550 9850 3550
Wire Wire Line
	9800 3650 9850 3650
Wire Wire Line
	9800 3750 9850 3750
Wire Wire Line
	10450 3550 10500 3550
Wire Wire Line
	10450 3650 10500 3650
Wire Wire Line
	10450 3750 10500 3750
Wire Wire Line
	9200 3250 9850 3250
Wire Wire Line
	9850 3250 9850 3550
Connection ~ 9850 3550
Wire Wire Line
	9850 3250 10500 3250
Wire Wire Line
	10500 3250 10500 3550
Connection ~ 9850 3250
Connection ~ 10500 3550
Wire Wire Line
	9200 3950 9850 3950
Wire Wire Line
	9850 3950 9850 3750
Connection ~ 9850 3750
Wire Wire Line
	10500 3950 10500 3750
Connection ~ 10500 3750
Wire Wire Line
	9850 3950 10500 3950
Connection ~ 9850 3950
Wire Wire Line
	9200 3550 9100 3550
Wire Wire Line
	9200 3650 9100 3650
Wire Wire Line
	9200 3750 9100 3750
Wire Wire Line
	9200 3950 9200 3750
Connection ~ 9200 3750
Wire Wire Line
	9200 3550 9200 3250
Connection ~ 9200 3550
Wire Wire Line
	9200 3250 8500 3250
Connection ~ 9200 3250
Connection ~ 8500 3250
Wire Wire Line
	9200 3950 8500 3950
Connection ~ 9200 3950
Connection ~ 8500 3950
$Comp
L Connector:Conn_01x03_Female J21
U 1 1 5F33970A
P 7500 4750
F 0 "J21" H 7450 5100 50  0000 L CNN
F 1 "neopixel_left" H 7350 4950 50  0000 L CNN
F 2 "Connector_JST:JST_EH_B3B-EH-A_1x03_P2.50mm_Vertical" H 7500 4750 50  0001 C CNN
F 3 "~" H 7500 4750 50  0001 C CNN
	1    7500 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	7300 4850 7250 4850
Wire Wire Line
	8500 3750 8500 3950
Wire Wire Line
	7300 4750 7250 4750
Wire Wire Line
	7300 4650 7250 4650
Text Label 7250 4650 2    50   ~ 0
5V
Text Label 7250 4850 2    50   ~ 0
GND
Text Label 7250 4750 2    50   ~ 0
neopixel_left
$Comp
L Connector:Conn_01x03_Female J22
U 1 1 5F38FD3E
P 8450 4750
F 0 "J22" H 8400 5100 50  0000 L CNN
F 1 "neopixel_right" H 8300 4950 50  0000 L CNN
F 2 "Connector_JST:JST_EH_B3B-EH-A_1x03_P2.50mm_Vertical" H 8450 4750 50  0001 C CNN
F 3 "~" H 8450 4750 50  0001 C CNN
	1    8450 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	8250 4850 8200 4850
Wire Wire Line
	8250 4750 8200 4750
Wire Wire Line
	8250 4650 8200 4650
Text Label 8200 4650 2    50   ~ 0
5V
Text Label 8200 4850 2    50   ~ 0
GND
Text Label 8200 4750 2    50   ~ 0
neopixel_right
$Comp
L Connector:Conn_01x03_Female J15
U 1 1 5F3B87A7
P 4600 7200
F 0 "J15" H 4450 7600 50  0000 L CNN
F 1 "GPIO" H 4400 7450 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x03_P2.54mm_Vertical" H 4600 7200 50  0001 C CNN
F 3 "~" H 4600 7200 50  0001 C CNN
	1    4600 7200
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x03_Female J16
U 1 1 5F3BE113
P 5050 7200
F 0 "J16" H 4850 7600 50  0000 L CNN
F 1 "PWR" H 4850 7450 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x03_P2.54mm_Vertical" H 5050 7200 50  0001 C CNN
F 3 "~" H 5050 7200 50  0001 C CNN
	1    5050 7200
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x03_Female J17
U 1 1 5F3D2E83
P 5500 7200
F 0 "J17" H 5300 7600 50  0000 L CNN
F 1 "GND" H 5300 7450 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x03_P2.54mm_Vertical" H 5500 7200 50  0001 C CNN
F 3 "~" H 5500 7200 50  0001 C CNN
	1    5500 7200
	1    0    0    -1  
$EndComp
Wire Wire Line
	5300 7100 5250 7100
Wire Wire Line
	5250 7100 5250 7200
Wire Wire Line
	5250 7200 5300 7200
Wire Wire Line
	5250 7200 5250 7300
Wire Wire Line
	5250 7300 5300 7300
Connection ~ 5250 7200
Wire Wire Line
	5250 7300 5250 7400
Connection ~ 5250 7300
Wire Wire Line
	4850 7100 4800 7100
Wire Wire Line
	4800 7100 4800 7200
Wire Wire Line
	4800 7300 4850 7300
Wire Wire Line
	4850 7200 4800 7200
Connection ~ 4800 7200
Wire Wire Line
	4800 7200 4800 7300
Connection ~ 4800 7300
Wire Wire Line
	4800 7300 4800 7400
Text Label 4800 7400 0    50   ~ 0
5V
Text Label 5250 7400 0    50   ~ 0
GND
Text Label 1300 2900 2    50   ~ 0
neopixel_right
Wire Wire Line
	4400 7100 4350 7100
Wire Wire Line
	4400 7200 4350 7200
Wire Wire Line
	4400 7300 4350 7300
Text Label 4350 7100 2    50   ~ 0
GPIO12
Text Label 4350 7200 2    50   ~ 0
GPIO07
Text Label 4350 7300 2    50   ~ 0
GPIO08
Wire Wire Line
	10500 3950 11100 3950
Wire Wire Line
	11100 3950 11100 3750
Connection ~ 10500 3950
Wire Wire Line
	10500 3250 11100 3250
Wire Wire Line
	11100 3250 11100 3550
Connection ~ 10500 3250
NoConn ~ 11100 3650
$Comp
L Connector:Conn_01x04_Female J8
U 1 1 5EF2061E
P 2950 4400
F 0 "J8" H 2950 4750 50  0000 R CNN
F 1 "HC-SR04" H 2950 4650 50  0000 R CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Vertical" H 2950 4400 50  0001 C CNN
F 3 "~" H 2950 4400 50  0001 C CNN
	1    2950 4400
	-1   0    0    -1  
$EndComp
$EndSCHEMATC
