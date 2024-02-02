#
# Copyright (C) 2022 Gagan Malvi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

# This requires host fastboot to be installed

import os
import subprocess

def flashPartition(partition, file):
    result = subprocess.run(['fastboot', 'flash', partition, file])
    return result.returncode

def wipeDevice():
    result = subprocess.run(['fastboot', '-w'])
    return result.returncode

def reboot():
    result = subprocess.run(['fastboot', 'reboot'])
    return result.returncode

def rebootRecovery():
    result = subprocess.run(['fastboot', 'reboot', 'recovery'])
    return result.returncode

def rebootBootloader():
    result = subprocess.run(['fastboot', 'reboot', 'bootloader'])
    return result.returncode

def rebootFastboot():
    result = subprocess.run(['fastboot', 'reboot', 'fastboot'])
    return result.returncode

def oemlock():
    result = subprocess.run(['fastboot', 'oem', 'lock'])
    return result.returncode

def oemlock2():
    result = subprocess.run(['fastboot', 'flashing', 'lock'])
    return result.returncode

def oemUnlock():
    result = subprocess.run(['fastboot', 'flashing', 'unlock'])
    return result

def oemUnlock2():
    result = subprocess.run(['fastboot', 'oem', 'unlock'])
    return result

