#
# Copyright (C) 2022 Gagan Malvi
#
# SPDX-Identifier: GPL-3.0-or-later
#

import tools.parse as parser
import tools.fastboot as fastboot
import tools.adb as adb
import tools.warnings as warnings
import sys
import os
from tabulate import tabulate

if sys.platform == "linux" or sys.platform == "linux2":
    clr = "clear"
elif sys.platform == "win32" or sys.platform == "cygwin" or sys.platform == "msys":
    clr = "cls"

line = ("\033[1;92m╔═"+57*"\033[1;92m═")
line2 = ("\033[1;92m║"+58*"\033[1;92m═")

def flash(scatter_file, location):
    try:
        os.chdir(location)
        print("\033[1;92m[-] Generating partition table...")
        scatter_content = parser.parse_scatter(scatter_file)
        partitions = parser.partition_list_generate(scatter_content)
        print(warnings.aboutwarning)

        # Ask the user for flashing option
        print("\033[1;92mChoose an option:")
        print("\033[1;93m1. Upgrade (without user data)")
        print("\033[1;93m2. Flash all (including user data)")
        choice = input("\033[1;92mSelect [1/2]: \033[1;97m")

        # Filter partitions based on user's choice
        partitions_to_flash = {}
        for case in partitions:
            # If upgrading, exclude user data partition
            if choice == "1" and "userdata" in case.lower():
                continue
            partitions_to_flash[case] = partitions[case]

        # Display partitions to flash
        partitionsList = []
        for case in partitions_to_flash:
            partitionsList.append([case, partitions_to_flash[case]])

        print(tabulate(partitionsList, headers=['Partition', 'Image'], tablefmt="fancy_grid"))
        
        a = input("\033[1;92m║ \033[1;93mContinue Flashing? [y/n]: \033[1;97m")
        if check_file(partitions=partitions_to_flash) and a.lower() == "y":
            print("\033[1;92m[-] Flashing images...")
            for case in partitions_to_flash:
                return_code = fastboot.flashPartition(partition=case, file=partitions_to_flash[case])
                if return_code == 0:
                    print(f"\033[1;92m[*] Flashed {case} successfully.\033[1;97m")
                else:
                    print(f"\033[1;91m[*] Flashing {case} failed with return code: {return_code}\033[1;97m")
            print(line)
            input("\033[1;92m║ \033[1;93mFinish.\033[1;97m")
            menu()
        else:
            menu()
    except Exception as e:
        print(f"\033[1;91m[Error] An unexpected error occurred: {e}\033[1;97m")




"""
def flash(scatter_file, location):
    try:
        os.chdir(location)
        print("\033[1;92m[-] Generating partition table...")
        scatter_content = parser.parse_scatter(scatter_file)
        partitions = parser.partition_list_generate(scatter_content)
        print(warnings.aboutwarning)

        partitionsList = []
        for case in partitions:
            partitionsList.append([case, partitions[case]])

        print(tabulate(partitionsList, headers=[
              'Partition', 'Image'], tablefmt="fancy_grid"))
        a = input("\033[1;92m║ \033[1;93mContinue Flashing?[y/n].\033[1;97m")
        if check_file(partitions=partitions) and a.lower() == "y":
            print("\033[1;92m[-] Flashing images...")
            for case in partitions:
                # fastboot.flashPartition(partition=case, file=partitions[case])
                # print("[*] Flashed " + case + " successfully.")
                return_code = fastboot.flashPartition(
                    partition=case, file=partitions[case])
                if return_code == 0:
                    print(
                        f"\033[1;92m[*] Flashed {case} successfully.\033[1;97m")
                else:
                    print(
                        f"\033[1;91m[*] Flashing {case} failed with return code: {return_code}\033[1;97m")
            print(line)
            input("\033[1;92m║ \033[1;93mFinish.\033[1;97m")
            menu()
        else:
            menu()
    except Exception as e:
        print(f"\033[1;91m[Error] An unexpected error occurred: {e}\033[1;97m")
"""


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
        print(
            "\033[1;92m║ \033[1;91mSome partitions is missing do you want to continue? [Y/n]")
        return True if isYes() else False

    return True


def wipe_device():
    print(
        "\033[1;92m║ \033[1;93mAre you sure Do you want to Wipe your device? [Y/n]")
    if isYes():
        result = fastboot.wipeDevice()
        if result == 0:
            print("\033[1;92m[-] Wipe device successfully.")
    else:
        print("Wipe device cancelled.")

    input("\033[1;93m Back to menu\033[1;97m")
    menu()


def reboot_device():
    print(
        "\033[1;92m║ \033[1;93mAre you sure Do you want to Reboot your device? [Y/n]")
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
    # I-print ang result para sa debugging
    print("Return Code:", result.returncode)
    print("Output:", result.stdout)
    print("Error:", result.stderr)
    if result.returncode != 0:
        print("\033[1;93m[-] First command failed.")
    else:
        print("\033[1;92m[-] Bootloader unlocked successfully.")

    input()
    menu()


def unlock_bootloader2():
    print("\033[1;92m[-] Unlocking bootloader...")
    # Subukan ang unang command
    result = fastboot.oemUnlock2()
    # I-check ang return code
    # I-print ang result para sa debugging
    print("Return Code:", result.returncode)
    print("Output:", result.stdout)
    print("Error:", result.stderr)
    if result.returncode != 0:
        print("\033[1;93m[-] First command failed.")
    else:
        print("\033[1;92m[-] Bootloader unlocked successfully.")
    input()
    menu()


def lock_bootloader():
    print("\033[1;92m[-] Unlocking bootloader...")
    # Subukan ang unang command
    result = fastboot.oemLock()
    # I-check ang return code
    print("Return Code:", result.returncode)
    print("Output:", result.stdout)
    print("Error:", result.stderr)
    if result.returncode != 0:
        print("\033[1;93m[-] First command failed.")
    else:
        print("\033[1;92m[-] Bootloader locked successfully.")

    input()
    menu()


def lock_bootloader2():
    print("\033[1;92m[-] Unlocking bootloader...")
    # Subukan ang unang command
    result = fastboot.oemLock2()
    # I-check ang return code
    print("Return Code:", result.returncode)
    print("Output:", result.stdout)
    print("Error:", result.stderr)
    if result.returncode != 0:
        print("\033[1;93m[-] First command failed.")
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

def get_slot():
    print("\033[1;92m║ \033[1;97mPartition Slot")
    print(
        "\033[1;92m║ \033[1;91m1. \033[1;94m—> \033[1;92mA")
    print(
        "\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mB")
    p = pick()
    if p == "1":
        return "a"
    elif p == "2":
        return "b"
    else:
        input(f"Partition slot {p} is invalid")
        menu()

def slot_changer(partitions, partition_slot):
    new_partitions = dict()
    for partition_name in partitions:
        if partition_name.endswith('_a') or partition_name.endswith('_b'):
            new_partition_name = partition_name[:-2] + '_' + partition_slot
        else:
            new_partition_name = partition_name
            
        new_partitions[new_partition_name] = partitions[partition_name]
    return new_partitions



def flash_ab(scatter_file, location, partition_slot):
    try:
        os.chdir(location)
        print("\033[1;92m[-] Generating partition table...")
        scatter_content = parser.parse_scatter(scatter_file)
        partitions = parser.partition_list_generate(scatter_content)
        print(warnings.aboutwarning)
        partitions = slot_changer(partitions=partitions, partition_slot=partition_slot)
        partitionsList = []
        for case in partitions:
            partitionsList.append([case, partitions[case]])

        print(tabulate(partitionsList, headers=[
              'Partition', 'Image'], tablefmt="fancy_grid"))
        a = input("\033[1;92m║ \033[1;93mContinue Flashing?[y/n].\033[1;97m")
        if check_file(partitions=partitions) and a.lower() == "y":
            print("\033[1;92m[-] Flashing images...")
            for case in partitions:
                # fastboot.flashPartition(partition=case, file=partitions[case])
                # print("[*] Flashed " + case + " successfully.")
                return_code = fastboot.flashPartition(
                    partition=case, file=partitions[case])
                if return_code == 0:
                    print(
                        f"\033[1;92m[*] Flashed {case} successfully.\033[1;97m")
                else:
                    print(
                        f"\033[1;91m[*] Flashing {case} failed with return code: {return_code}\033[1;97m")
            # Palitan ang default boot slot matapos ang flash
            fastboot.change_boot_slot(partition_slot)
            print(line)
            input("\033[1;92m║ \033[1;93mFinish.\033[1;97m")
            menu()
        else:
            menu()
    except Exception as e:
        print(f"\033[1;91m[Error] An unexpected error occurred: {e}\033[1;97m")

def erase_partition():
    print("\033[1;92m║ \033[1;97mPartition Name:")
    partition_name = pick()
    result = fastboot.erasePartition(partition=partition_name)
    print("Return Code:", result.returncode)
    print("Output:", result.stdout)
    print("Error:", result.stderr)
    input()
    menu()


def menu_pick():
    p = pick()
    if p == "1":
        scatter_file, location = get_scatter_file()
        flash(scatter_file=scatter_file, location=location)
    if p == "2":
        scatter_file, location = get_scatter_file()
        slot = get_slot()
        flash_ab(scatter_file=scatter_file, location=location, partition_slot=slot)
    elif p == "3":
        unlock_bootloader()
    elif p == "4":
        unlock_bootloader2()
    elif p == "5":
        lock_bootloader()
    elif p == "6":
        lock_bootloader2()
    elif p == "7":
        fastboot.rebootRecovery()
    elif p == "8":
        fastboot.rebootFastboot()
    elif p == "9":
        fastboot.rebootBootloader()
    elif p == "10":
        erase_partition()
    elif p == "11":
        if are_you_sure():
            fastboot.wipeDevice()
            input()
            menu()
        else:
            menu()
    elif p == "12":
        if are_you_sure():
            fastboot.eraseCache()
            input()
            menu()
        else:
            menu()
    elif p == "13":
        slot = get_slot()
        fastboot.change_boot_slot(slot=slot)
        input("Back")
        menu()
    elif p == "14":
        fastboot.reboot()
    elif p == "00":
        os.system("git pull")
        os.system("python3 main.py")
    elif p == "0":
        sys.exit()
    else:
        print("\033[1;92m║ \033[1;91minvalid input")
        menu_pick()

def are_you_sure():
    a = input("\033[1;92m║ Are you sure? this my brick your device[y/n]")
    try:
        if a.lower() == "y" or str(a[0]).lower() == "y":
            return True
        else:
            print("\033[1;92m║ Cancelled.")
            return False
    except:
        return False
def pick():
    a = input("\033[1;92m╚═════\033[1;91m: \033[1;97m")
    return a


def menu():
    os.system(clr)
    print(line)
    print("\033[1;92m║ \033[1;91m1. \033[1;94m—> \033[1;92mFlash ROM[Scatter file]")
    print("\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mFlash ROM[Scatter file][A/B slot]")
    print(
        "\033[1;92m║ \033[1;91m3. \033[1;94m—> \033[1;92mUnlock bootloader[Method 1]")
    print(
        "\033[1;92m║ \033[1;91m4. \033[1;94m—> \033[1;92mUnlock bootloader[Method 2]")
    print(
        "\033[1;92m║ \033[1;91m5. \033[1;94m—> \033[1;92mLock bootloader[Method 1]")
    print(
        "\033[1;92m║ \033[1;91m6. \033[1;94m—> \033[1;92mLock bootloader[Method 2]")
    print("\033[1;92m║ \033[1;91m7. \033[1;94m—> \033[1;92mReboot Recovery")
    print("\033[1;92m║ \033[1;91m8. \033[1;94m—> \033[1;92mReboot Fastboot")
    print("\033[1;92m║ \033[1;91m9. \033[1;94m—> \033[1;92mReboot Bootloader")
    print("\033[1;92m║ \033[1;91m10. \033[1;94m—> \033[1;92mErase Partition")
    print("\033[1;92m║ \033[1;91m11. \033[1;94m—> \033[1;92mWipe device")
    print("\033[1;92m║ \033[1;91m12. \033[1;94m—> \033[1;92mErase cache")
    print("\033[1;92m║ \033[1;91m13. \033[1;94m—> \033[1;92mChange boot slot")
    print("\033[1;92m║ \033[1;91m14. \033[1;94m—> \033[1;92mReboot")
    print("\033[1;92m║ \033[1;91m00. \033[1;94m—> \033[1;92mUpdate")
    print("\033[1;92m║ \033[1;91m0. \033[1;94m—> \033[1;93mExit")
    menu_pick()


if __name__ == "__main__":
    menu()
