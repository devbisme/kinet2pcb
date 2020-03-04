EESchema Schematic File Version 4
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
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
L Device:C C1
U 1 1 5DBC3998
P 5375 3100
F 0 "C1" H 5490 3146 50  0000 L CNN
F 1 "C" H 5490 3055 50  0000 L CNN
F 2 "Capacitor_SMD:CP_Elec_5x3" H 5413 2950 50  0001 C CNN
F 3 "~" H 5375 3100 50  0001 C CNN
	1    5375 3100
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D1
U 1 1 5DBC3E23
P 5375 2600
F 0 "D1" V 5414 2483 50  0000 R CNN
F 1 "LED" V 5323 2483 50  0000 R CNN
F 2 "LED_SMD:LED_0201_0603Metric" H 5375 2600 50  0001 C CNN
F 3 "~" H 5375 2600 50  0001 C CNN
	1    5375 2600
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R1
U 1 1 5DBC51E3
P 5025 2825
F 0 "R1" H 5095 2871 50  0000 L CNN
F 1 "R" H 5095 2780 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 4955 2825 50  0001 C CNN
F 3 "~" H 5025 2825 50  0001 C CNN
	1    5025 2825
	1    0    0    -1  
$EndComp
Wire Wire Line
	5375 2450 5025 2450
Wire Wire Line
	5025 2450 5025 2675
Wire Wire Line
	5025 3375 5375 3375
Wire Wire Line
	5375 3375 5375 3250
Wire Wire Line
	5375 2950 5375 2750
Wire Wire Line
	5025 2975 5025 3375
$EndSCHEMATC
