#!/usr/bin/env python3
from datetime import datetime
import sys
import subprocess
import os
import pifacecad

GET_IP_CMD = "hostname --all-ip-addresses"
GET_TEMP_CMD = "/opt/vc/bin/vcgencmd measure_temp"
TOTAL_MEM_CMD = "free | grep 'Mem' | awk '{print $2}'"
USED_MEM_CMD = "free | grep '\-\/+' | awk '{print $3}'"

cum_dt=datetime.utcnow()
go_dt=datetime.utcnow()
kommen_counter=0
kommen_flag=False

temperature_symbol = pifacecad.LCDBitmap(
    [0x4, 0x4, 0x4, 0x4, 0xe, 0xe, 0xe, 0x0])
memory_symbol = pifacecad.LCDBitmap(
    [0xe, 0x1f, 0xe, 0x1f, 0xe, 0x1f, 0xe, 0x0])
temp_symbol_index, memory_symbol_index = 0, 1

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def get_my_ip():
    return run_cmd(GET_IP_CMD)[:-1]

def get_my_temp():
    return run_cmd(GET_TEMP_CMD)[5:9]

def get_my_free_mem():
    total_mem = float(run_cmd(TOTAL_MEM_CMD))
    used_mem = float(run_cmd(USED_MEM_CMD))
    mem_perc = used_mem / total_mem
    return "{:.1%}".format(mem_perc)

def show_sysinfo(event):
    ip = ""
    ip = get_my_ip()
    #event.chip.lcd.set_cursor(0,0)
    if len(ip) > 0:
        cad.lcd.clear()
        cad.lcd.write("IP:{}\n".format(get_my_ip()))
    else:
        cad.lcd.clear()
        cad.lcd.write("Waiting for IP..\n")
    #event.chip.lcd.set_cursor(0,1)
    cad.lcd.write_custom_bitmap(temp_symbol_index)
    cad.lcd.write(":{}C ".format(get_my_temp()))
    cad.lcd.write_custom_bitmap(memory_symbol_index)
    cad.lcd.write(":{}".format(get_my_free_mem()))

def calc_work_time(start,ende):
    calc_time=ende-start
    #if calc_time
    return calc_time

def kommen(event):
    global cum_dt
    cum_dt=datetime.utcnow()
    global kommen_flag
    kommen_flag=True
    global kommen_counter
    kommen_counter+=1
    event.chip.lcd.clear()
    event.chip.lcd.set_cursor(0,0)
    event.chip.lcd.write('-----Kommen-----')
def gehen(event):
    global go_dt
    global cum_dt
    global kommen_flag
    event.chip.lcd.clear()
    event.chip.lcd.set_cursor(0,0)
    if kommen_flag:
        go_dt=datetime.utcnow()
        event.chip.lcd.write('------Gehen-----')
        event.chip.lcd.set_cursor(0,1)
        event.chip.lcd.write(str(calc_work_time(cum_dt,go_dt)))
        kommen_flag=False
    else:
        event.chip.lcd.write('Noch nicht')
        event.chip.lcd.set_cursor(0,1)
        event.chip.lcd.write('eingestempelt!')
def calc(event):
    event.chip.lcd.clear()
    global cum_dt
    global go_dt
    event.chip.lcd.set_cursor(0,0)
    if kommen_flag and kommen_counter>0:
        event.chip.lcd.write('Aktuelle Zeit:')
        event.chip.lcd.set_cursor(0,1)
        event.chip.lcd.write(str(calc_work_time(cum_dt,datetime.utcnow())))
    elif kommen_counter==0:
        event.chip.lcd.write('Noch nicht')
        event.chip.lcd.set_cursor(0,1)
        event.chip.lcd.write('eingestempelt!')
    else:
        event.chip.lcd.write('Letzte Zeit war:')
        event.chip.lcd.set_cursor(0,1)
        event.chip.lcd.write(str(calc_work_time(cum_dt,go_dt)))
def clearit(event):
    event.chip.lcd.clear()

cad = pifacecad.PiFaceCAD()
cad.lcd.clear()
cad.lcd.write('Willkommen zur')
cad.lcd.set_cursor(0,1)
cad.lcd.write('Zeiterfassung!')
cad.lcd.store_custom_bitmap(temp_symbol_index, temperature_symbol)
cad.lcd.store_custom_bitmap(memory_symbol_index, memory_symbol)
listener = pifacecad.SwitchEventListener(chip=cad)
listener.register(0, pifacecad.IODIR_FALLING_EDGE, kommen)
listener.register(1, pifacecad.IODIR_FALLING_EDGE, calc)
listener.register(2, pifacecad.IODIR_FALLING_EDGE, gehen)
listener.register(3, pifacecad.IODIR_FALLING_EDGE, show_sysinfo)
listener.register(4, pifacecad.IODIR_FALLING_EDGE, clearit)
listener.activate()
