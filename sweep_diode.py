#!/usr/bin/env python3
"""
Sweep voldate for automatic I-V characterization
"""

import serial
import time
import numpy as np
import matplotlib.pyplot as plt

def set_voltage_sweep(conn: serial.Serial, v1: float, v2: float, npoints: int) -> None:
    """ Set source voltage sweep
    """
    cmd = 'SYSTem:FUNCtion:MODE SOURCEVOLTage;' + \
       ':SOURce:VOLTage:CURRent:LIMit 0.3A;' + \
        ':SOURce:VOLTage:MEASure:PRIMary VOLTage;' + \
        ':SOURce:VOLTage:MEASure:SECondary CURRent;' + \
        ':SOURce:VOLTage:SHAPe SWEep;' + \
        ':SOURce:VOLTage:SWEep:SPACing LINear;' + \
        ':SOURce:VOLTage:SWEep:POINts ' + str(npoints) + ';' + \
        ':SOURce:VOLTage:SWEep:APERture:TIME 0.5S;' + \
        ':SOURce:VOLTage:SWEep:STARt ' + str(v1) + 'V;' + \
        ':SOURce:VOLTage:SWEep:STOP ' + str(v2) + 'V;\n'
    conn.write(cmd.encode())


if __name__ == '__main__':
    conn = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
    set_voltage_sweep(conn, -8.0, 1.0, 100)
    conn.write('OUTput:STATe 1\n'.encode())
    time.sleep(60)
    conn.write('MEMory:DATA:BUFFer:INFO?\n'.encode())
    npts = eval(conn.readline().decode().split(',')[1])
    #conn.write('MEMory:DATA:BUFFer:BINary? 0,50\n'.encode())
    conn.write('MEMory:DATA:BUFFer:ASCii?\n'.encode())
    data_pts = np.array([eval(i) for i in conn.readline().decode().split(',')]).reshape(npts,3)
    plt.plot(data_pts[:,0], data_pts[:,1])
    plt.grid(True)

    plt.savefig('diode.png')

    
    
