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

# Parse MTK scatterfile and generate a list of partitions

import yaml
import re

def parse_scatter(path):
    with open(path, "r") as f:
        scatter_content = f.read()
        return scatter_content

def partition_list_generate(scatter_content):
    partitions = {}
    partition_pattern = re.compile(r'-\s+partition_index:\s+(\w+).*?partition_name:\s+(\w+).*?file_name:\s+([^\n]+).*?is_download:\s+(\w+)', re.DOTALL)
    matches = partition_pattern.findall(scatter_content)
    
    for match in matches:
        partition_index, partition_name, file_name, is_download = match
        if is_download.lower() == 'true':
            partitions[partition_name] = file_name.strip()

    return partitions