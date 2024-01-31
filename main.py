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
from tabulate import tabulate

def flash(path):
    print("[-] Generating partition table...")
    scatter_content = parser.parse_scatter(path)
    partitions = parser.partition_list_generate(scatter_content)
    print(warnings.aboutwarning)

    partitionsList = []
    for case in partitions:
        partitionsList.append([case, partitions[case]])

    print(tabulate(partitionsList, headers=['Partition', 'Image'], tablefmt="fancy_grid"))

    print("[-] Flashing images...")
    for case in partitions:
        fastboot.flashPartition(case, partitions[case])
        print("[*] Flashed " + case + " successfully.")
    p=input("Do you want to Wipe your device? [Y/n]")
    
    if p == "Y" or p == "y" or p[0] == "y":
        fastboot.wipeDevice()
    else:
        print("Wipe device canselled.")
        
    p=input("Do you want to reboot your device? [Y/n]")
    if p == "Y" or p == "y" or p[0] == "y":
        fastboot.reboot()
    else:
        print("Reboot device canselled.")
    print("\033[1;93m Finish.\033[1;97m")
if __name__ == "__main__":
    if len(sys.argv) > 1:
        flash(sys.argv[1])
    else:
        print("[-] Please provide a path to the scatter file in the SP Flash package.")

