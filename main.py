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
    elif p == "2":
        unlock_bootloader()
    elif p == "3":
        unlock_bootloader2()
    elif p == "4":
        lock_bootloader()
    elif p == "5":
        lock_bootloader2()
    elif p == "6":
        fastboot.rebootRecovery()
    elif p == "7":
        fastboot.rebootFastboot()
    elif p == "8":
        fastboot.rebootBootloader()
    elif p == "9":
        erase_partition()
    elif p == "10":
        if are_you_sure():
            fastboot.wipeDevice()
            input()
            menu()
        else:
            menu()
    elif p == "11":
        if are_you_sure():
            fastboot.eraseCache()
            input()
            menu()
        else:
            menu()
    elif p == "12":
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
    print(
        "\033[1;92m║ \033[1;91m2. \033[1;94m—> \033[1;92mUnlock bootloader[Method 1]")
    print(
        "\033[1;92m║ \033[1;91m3. \033[1;94m—> \033[1;92mUnlock bootloader[Method 2]")
    print(
        "\033[1;92m║ \033[1;91m4. \033[1;94m—> \033[1;92mLock bootloader[Method 1]")
    print(
        "\033[1;92m║ \033[1;91m5. \033[1;94m—> \033[1;92mLock bootloader[Method 2]")
    print("\033[1;92m║ \033[1;91m6. \033[1;94m—> \033[1;92mReboot Recovery")
    print("\033[1;92m║ \033[1;91m7. \033[1;94m—> \033[1;92mReboot Fastboot")
    print("\033[1;92m║ \033[1;91m8. \033[1;94m—> \033[1;92mReboot Bootloader")
    print("\033[1;92m║ \033[1;91m9. \033[1;94m—> \033[1;92mErase Partition")
    print("\033[1;92m║ \033[1;91m10. \033[1;94m—> \033[1;92mWipe device")
    print("\033[1;92m║ \033[1;91m11. \033[1;94m—> \033[1;92mErase cache")
    print("\033[1;92m║ \033[1;91m12. \033[1;94m—> \033[1;92mReboot")
    print("\033[1;92m║ \033[1;91m00. \033[1;94m—> \033[1;92mUpdate")
    print("\033[1;92m║ \033[1;91m0. \033[1;94m—> \033[1;93mExit")
    menu_pick()


if __name__ == "__main__":
    menu()
