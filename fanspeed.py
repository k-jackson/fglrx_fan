#!/usr/bin/env python
from subprocess import call
import time
import subprocess
import shlex
import daemon

# These are the variables used to hold the fan speed (percentages)
# and temperatures at which they are activated. Modify these according 
# to your GPU's requirements.
current_fan = 20
temps = [55,60,64,70,90]
fanspeeds = [20,35,50,60,80]

# Set the GPU fan speed through aticonfig
def fan_spd(speed_int):
    # shlex.split: outputs command as list of strings
    c_list = shlex.split('aticonfig --pplib-cmd "set fanspeed 0 ' +
            str(speed_int) + '"')
    call(c_list)
    current_fan = int(speed_int)
    
# Request the current main GPU temperature from aticonfig
def get_temp():
    c_list = shlex.split('aticonfig --adapter=0 --od-gettemperature')
    output = subprocess.check_output(c_list)
    index = output.find('.00')
    temp = output[index-2:index]
    temp = int(temp)

    # Because aticonfig has troubles predictable returning 
    # accurate values > 100*C, we only return those that are below
    # that number. The 'temps' and 'fanspeeds' arrays should 
    # be set to prevent the GPU from reaching the point where 
    # they would likely be on fire, but the hardware failsafes exist
    # to CYA in case of such an unlikely scenario.
    if temp < 100:
        return temp

def auto_fan_spd():
    fan_spd(fanspeeds[0])

    # Over a 5-second interval, check whether the fan speed should be
    # updated or not.
    while True:
        temperature = get_temp()
        if (temperature < temps[0] and current_fan != fanspeeds[0]):
            fan_spd(fanspeeds[0])
        elif (temperature > temps[0] and temperature < temps[1] and
        current_fan != fanspeeds[1]):
            fan_spd(fanspeeds[1])
        elif (temperature > temps[1] and temperature < temps[2]
        and current_fan != fanspeeds[2]):
            fan_spd(fanspeeds[2])
        elif (temperature > temps[2] and temperature < temps[3] and
                current_fan != fanspeeds[3]):
            fan_spd(fanspeeds[3])
        elif (temperature > temps[3] and current_fan != fanspeeds[4]):
            fan_spd(fanspeeds[4])

        time.sleep(5)

# Run the script as a background process
with daemon.DaemonContext():
    auto_fan_spd()



