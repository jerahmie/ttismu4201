#!/usr/bin/env python3
"""
SCPI Commands 
Aim TTi SMU4201
"""
import serial
import time

IDN = '*IDN?\n' 
FW = 'FW?\n'
MAC = 'MAC_ID?\n'

def scpi_send(conn: serial.Serial, cmd: str) -> str:
    """
    send command to device
    """
    conn.write(cmd.encode())
    return conn.readline().decode()

def set_source_voltage(conn: serial.Serial, vref: float=0.0) -> None:
    """
    Update source voltage
    """
    # ':SOURce:VOLTage:SHAPe:COUNt:INFinit 1;' + \
    cmd = 'SYSTem:FUNCtion:MODE SOURCEVOLTage;' + \
          ':SOURce:VOLTage:CURRent:LIMit 1.0 A;' + \
          ':SOURce:VOLTage:MEASure:PRIMary CURRent;'+ \
          ':SOURce:VOLTage:MEASure:SECondary VOLTage;' + \
          ':SOURce:VOLTage:SHAPe FIXed;' + \
          ':SOURce:VOLTage:FIXed:APERture:TIME 1S;' + \
          ':SOURce:VOLTage:FIXed:LEVel ' + str(vref) + '\n'
    conn.write(cmd.encode())

def sense_current_terminals(conn: serial.Serial) -> str:
    """
    Query the measure current mode terminals
    """
    cmd = 'SYSTem:FUNCtion:MODE MEASURECURRent;' + \
        ':SENSe:CURRent:TERMinals?\n'

    conn.write(cmd.encode())
    return conn.readline().decode()

def measure_current(conn: serial.Serial): 
    """
    """
    cmd = 'SYSTem:FUNCtion:MODE MEASURECURRent;' + \
        ':MEASure:PRIMary:LIVEdata?\n'
    conn.write(cmd.encode())
    return conn.readline().decode()
    
if __name__ == '__main__':
    conn = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
    #print(scpi_send(conn, IDN))
    print(sense_current_terminals(conn))
    for vref in [3.]:
        set_source_voltage(conn, vref)
        conn.write('OUTPut:STATe 1\n'.encode())
        #print(measure_current(conn))
        time.sleep(2)
        conn.write('MEMory:DATA:BUFFer:ASCii?\n'.encode())
        print(conn.readline().decode())
        

