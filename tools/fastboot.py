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

def change_boot_slot(slot):
    """
    Changes the active boot slot of the device using fastboot command.

    Args:
        slot (str): The slot to set as active (e.g., 'a', 'b').

    Returns:
        int: Return code of the fastboot command (0 if successful, non-zero otherwise).
    """
    result = subprocess.run(['fastboot', f'--set-active={slot}'])
    
    # Check if fastboot command was successful
    if result.returncode == 0:
        print(f"Boot slot changed to {slot} successfully.")
    else:
        print(f"Failed to change boot slot to {slot}. Error code: {result.returncode}")

    return result.returncode


def check_device_details():
    # Check current slot
    current_slot = subprocess.run(['fastboot', 'getvar', 'current-slot'], capture_output=True, text=True).stdout.strip()
    
    # Check firmware version
    firmware_version = subprocess.run(['fastboot', 'getvar', 'version'], capture_output=True, text=True).stdout.strip()
    
    # Check other device details using fastboot commands
    device_model = subprocess.run(['fastboot', 'getvar', 'product'], capture_output=True, text=True).stdout.strip()
    device_id = subprocess.run(['fastboot', 'getvar', 'serialno'], capture_output=True, text=True).stdout.strip()
    os_version = subprocess.run(['fastboot', 'getvar', 'version'], capture_output=True, text=True).stdout.strip()
    build_number = subprocess.run(['fastboot', 'getvar', 'buildno'], capture_output=True, text=True).stdout.strip()
    kernel_version = subprocess.run(['fastboot', 'getvar', 'kernel'], capture_output=True, text=True).stdout.strip()

    # Format and print the device details
    device_details = {
        "Current Slot": current_slot,
        "Firmware Version": firmware_version,
        "Device Model": device_model,
        "Device ID": device_id,
        "Operating System Version": os_version,
        "Build Number": build_number,
        "Kernel Version": kernel_version
        # Add more details as needed
    }
    print("Device Details:")
    for key, value in device_details.items():
        print(f"{key}: {value}")