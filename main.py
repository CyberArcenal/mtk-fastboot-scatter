#
# Copyright (C) 2022 Gagan Malvi
#
# SPDX-Identifier: GPL-3.0-or-later
#

import tools.parse as parser
import tools.fastboot as fastboot
import tools.adb as adb
import tools.warnings as warnings
import sys, os
from tabulate import tabulate

if sys.platform == "linux" or sys.platform == "linux2":
    clr="clear"
elif sys.platform == "win32" or sys.platform == "cygwin" or sys.platform == "msys":
    clr="cls"

line=("\033[1;92m╔═"+57*"\033[1;92m═")
line2=("\033[1;92m║"+58*"\033[1;92m═")


def flash(scatter_file, location):
    os.chdir(location)
    print("\033[1;92m[-] Generating partition table...")
    scatter_content = parser.parse_scatter(scatter_file)
    partitions = parser.partition_list_generate(scatter_content)
    print(warnings.aboutwarning)

    partitionsList = []
    for case in partitions:
        partitionsList.append([case, partitions[case]])

    print(tabulate(partitionsList, headers=['Partition', 'Image'], tablefmt="fancy_grid"))
    
    if check_file(partitions=partitions):
        print("\033[1;92m[-] Flashing images...")
        for case in partitions:
            fastboot.flashPartition(partition=case, file=partitions[case])
            print("[*] Flashed " + case + " successfully.")
        
        print("\033[1;93m Finish.\033[1;97m")
    else:
        menu()

def isYes():
    p = pick()
    try:
        if p.lower() == "y" or p[0].lower() == "y":
            return True
    except:
        pass
        
    return False

def check_file(partitions):
    m = False
    for f in partitions:
        file_path = os.path.join(partitions[f])
        if not os.path.exists(file_path):
            print(f"\033[1;92m║ \033[1;97m{partitions[f]} \033[1;93mmissing")
            m = True
    if m:
        print("\033[1;92m║ \033[1;91mSome partitions is missing do you want to continue? [Y/n]")
        return True if isYes() else False
    
    return True

def wipe_device():
    print("\033[1;92m║ \033[1;93mAre you sure Do you want to Wipe your device? [Y/n]")
    if isYes():
        result = fastboot.wipeDevice()
        if result == 0:
            print("\033[1;92m[-] Wipe device successfully.")
    else:
        print("Wipe device cancelled.")
    
    input("\033[1;93m Back to menu\033[1;97m")
    menu()

def reboot_device():
    print("\033[1;92m║ \033[1;93mAre you sure Do you want to Reboot your device? [Y/n]")
    if isYes():
        result = fastboot.reboot()
        if result == 0:
            print("\033[1;92m[-] Reboot device successfully.")
    else:
        print("Reboot device cancelled.")
    
    input("\033[1;93m Back to menu\033[1;97m")
    menu()

def unlock_bootloader():
    print("\033[1;92m[-] Unlocking bootloader...")
    # Subukan ang unang command
    result = fastboot.oemUnlock()
    # I-check ang return code
    if result.returncode != 0:
        print("\033[1;93m[-] First command failed. Trying second command...")
        
        # Subukan ang pangalawang command
        result = fastboot.oemUnlock2()
        
        # I-print ang result para sa debugging
        print("Return Code:", result.returncode)
        print("Output:", result.stdout)
        print("Error:", result.stderr)
        
        # I-check kung ang pangalawang command ay nagtagumpay
        if result.returncode == 0:
            print("\033[1;92m[-] Bootloader unlocked successfully.")
        else:
            print("\033[1;91m[-] Bootloader unlocking failed.")
    else:
        print("\033[1;92m[-] Bootloader unlocked successfully.")
        
    input()
    menu()
    
def lock_bootloader():
    print("\033[1;92m[-] Unlocking bootloader...")
    # Subukan ang unang command
    result = fastboot.oemlock()
    # I-check ang return code
    if result.returncode != 0:
        print("\033[1;93m[-] First command failed. Trying second command...")
        
        # Subukan ang pangalawang command
        result = fastboot.oemlock2()
        
        # I-print ang result para sa debugging
        print("Return Code:", result.returncode)
        print("Output:", result.stdout)
        print("Error:", result.stderr)
        
        # I-check kung ang pangalawang command ay nagtagumpay
        if result.returncode == 0:
            print("\033[1;92m[-] Bootloader locked successfully.")
        else:
            print("\033[1;91m[-] Bootloader locking failed.")
    else:
        print("\033[1;92m[-] Bootloader locked successfully.")
        
    input()
    menu()
    
def get_scatter_file():
    print("\033[1;92m║ \033[1;97mScatter file")
    file = pick()
    if not os.path.exists(file):
        input(f"The file '{file}' does not exist.")
        menu()
        
    file_location = os.path.dirname(file)
    return file, file_location

def menu_pick():
    p = pick()
    if p == "1":
        scatter_file, location = get_scatter_file()
        flash(scatter_file=scatter_file, location=location)
    if p == "2":
        unlock_bootloader()
    elif p == "3":
        lock_bootloader()
    elif p == "4":
        wipe_device()
    elif p == "5":
        reboot_device()
    elif p == "0":
        sys.exit()
    else:
        print("\033[1;92m║ \033[1;91minvalid input")
        menu_pick()
        
def pick():
    a = input("\033[1;92m╚═════\033[1;91m: \033[1;97m")
    return a

def menu():
    print(line)
    print("\033[1;92m║ \033[1;91m1. \033[1;94m—> \033[1;92mFlash ROM with scatter file")
    print("\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mUnlock bootloader")
    print("\033[1;92m║ \033[1;91m3. \033[1;94m—> \033[1;92mLock bootloader")
    print("\033[1;92m║ \033[1;91m4. \033[1;94m—> \033[1;92mWipe device")
    print("\033[1;92m║ \033[1;91m5. \033[1;94m—> \033[1;92mReboot device")
    print("\033[1;92m║ \033[1;91m0. \033[1;94m—> \033[1;93mExit")
    menu_pick()

if __name__ == "__main__":
    menu()
    # if len(sys.argv) > 1:
    #     flash(sys.argv[1])
    # else:
    #     print("[-] Please provide a path to the scatter file in the SP Flash package.")

