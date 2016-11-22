#!/usr/bin/env python
from datetime import datetime
import os
import pifacecad

cum_dt=datetime.utcnow()
go_dt=datetime.utcnow()
kommen_counter=0
kommen_flag=False

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
    event.chip.lcd.write('Kommen saved!')
def gehen(event):
    global go_dt
    global cum_dt
    global kommen_flag
    event.chip.lcd.clear()
    event.chip.lcd.set_cursor(0,0)
    if kommen_flag:
        go_dt=datetime.utcnow()
        event.chip.lcd.write('Gehen saved!')
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
listener = pifacecad.SwitchEventListener(chip=cad)
listener.register(0, pifacecad.IODIR_FALLING_EDGE, kommen)
listener.register(1, pifacecad.IODIR_FALLING_EDGE, calc)
listener.register(2, pifacecad.IODIR_FALLING_EDGE, gehen)
listener.register(3, pifacecad.IODIR_FALLING_EDGE, clearit)
#listener.register(4, pifacecad.IODIR_RISING_EDGE, os.system('sudo poweroff'))
listener.activate()
