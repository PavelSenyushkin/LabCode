import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import time
from pylablib.devices import Ophir
import os
import sys
import ctypes
import time
import numpy as np
import matplotlib.pyplot as plt
from ctypes import byref
from ctypes import *
from scipy.optimize import curve_fit
import qcodes_contrib_drivers.drivers
from qcodes_contrib_drivers.drivers.Thorlabs.K10CR1 import Thorlabs_K10CR1
print('connecting to k10cr1 rotator')
apt = qcodes_contrib_drivers.drivers.Thorlabs.private.APT.Thorlabs_APT()
inst = Thorlabs_K10CR1("K10CR1", 0, apt)
print('connected')
print(inst._get_position())
inst.move_home()
print('homed')
ser = serial.Serial(   'COM11', 38400, timeout=0.01, bytesize=8, parity='N', stopbits=1)
meter = Ophir.VegaPowerMeter(("COM6", 115200))
print('connected to powermeter')
ser.reset_input_buffer()
inst.move_direction('fwd')
print('started jogging')


print("🧹 Очистка буферов...")
ser.reset_input_buffer()   # Arduino буфер
ser.reset_output_buffer()  # Выходной буфер
time.sleep(0.5)   



start_time = time.time()
current_time = datetime.datetime.now()
x = str(current_time.year) +'_'+ str(current_time.month)+'_'+ str(current_time.day) +'_'+ str(current_time.hour) +'_'+ str(current_time.minute)+'_'+ str(current_time.second)
with open(x + str('test_rotation') + str(20) + 's'+ '.txt', 'w') as file:
    while(time.time()- start_time <= 20):
        try:
            
            # Чтение данных из COM порта
            if ser.in_waiting:
                line_data = ser.readline().decode('utf-8').rstrip()
                
                try:
                    ser.flushInput()
                    time.sleep(0.015)
                    value = float(line_data)
                    
                    power = meter.get_power()
                    current_time2 = time.time()
                    #print(value / 10e-3, (current_time2-current_time1)/2)
                    t1 = start_time #time.strftime("%H:%M:%S", time.localtime(start_time)) 
                    t2 = current_time2 #time.strftime("%H:%M:%S", time.localtime(current_time2))
                    line = f"Countrate: {value / 10e-3:.1f}, Power: {power}, Start Time: {t1}, End_time: {t2}\n"
                    file.write(line)
                    file.flush() 
                    # print(power)  
                    
                except ValueError:
                    print(f"Ошибка преобразования: {line_data}")

        except Exception as e:
            print(f"Ошибка: {e}")
    inst.stop()
    print(inst._get_position())
    print('measurement time is over')
inst.close()
apt.apt_clean_up()
meter.close()
ser.close()