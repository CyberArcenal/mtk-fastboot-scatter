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

import subprocess

# Flashing commands
def flashPartition(partition, file):
    result = subprocess.run(['fastboot', 'flash', partition, file])
    return result.returncode

def erasePartition(partition):
    result = subprocess.run(['fastboot', 'erase', partition])
    return result.returncode

# Wipe commands
def wipeDevice():
    result = subprocess.run(['fastboot', '-w'])
    return result.returncode

def eraseCache():
    result = subprocess.run(['fastboot', 'erase', 'cache'])
    return result.returncode

# Reboot commands
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

# Lock/Unlock bootloader commands
def oemLock():
    result = subprocess.run(['fastboot', 'oem', 'lock'])
    return result.returncode

def oemUnlock():
    result = subprocess.run(['fastboot', 'oem', 'unlock'])
    return result.returncode

def oemLock2():
    result = subprocess.run(['fastboot', 'flashing', 'lock'])
    return result.returncode

def oemUnlock2():
    result = subprocess.run(['fastboot', 'flashing', 'unlock'])
    return result.returncode

def check_bootloader_status():
    result = subprocess.run(['fastboot', 'getvar', 'unlocked'], capture_output=True, text=True)
    output = result.stdout.strip().lower()
    return "unlocked: yes" in output


