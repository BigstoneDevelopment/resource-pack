import os
import json
import sys
import copy
import math

n = 1535
tileSize = 0.3125
tileScale = 0.5

script_dir = os.path.dirname(os.path.abspath(__file__))

#tri left
tri_left_ref = os.path.join(script_dir, 'models', 'item', "tri_left.json")
print("ref:"+tri_left_ref+"\n")
if not os.path.isfile(tri_left_ref):
    sys.exit("Error, can't find script")
print("found display reference 1 in "+tri_left_ref+"\n")

with open(tri_left_ref, 'r') as f1:
    tri_left = json.load(f1)

#tri right
tri_right_ref = os.path.join(script_dir, 'models', 'item', "tri_right.json")
print("ref:"+tri_right_ref+"\n")
if not os.path.isfile(tri_right_ref):
    sys.exit("Error, can't find script")
print("found display reference 2 in "+tri_right_ref+"\n")

with open(tri_right_ref, 'r') as f2:
    tri_right = json.load(f2)

output_dir = os.path.join(script_dir, 'models', 'item', 'component_item')
os.makedirs(output_dir, exist_ok=True)

def clampArray(ar):
    ar[0] = round(ar[0],2)
    ar[1] = round(ar[1],2)
    ar[2] = round(ar[2],2)

    ar[0] = min(max(ar[0],-16),32)
    ar[1] = min(max(ar[1],-16),32)
    ar[2] = min(max(ar[2],-16),32)

vert_scale = 0.625
vert_base_count = 33
hori_count = 32

count = 0
for i in range(hori_count):

    invert_threshold = 16-0.5
    add_height = math.floor((invert_threshold - abs(i - invert_threshold))*2)
    print(f"i: {i}, j: {vert_base_count+add_height}\n")
    for j in range(vert_base_count + add_height):

        tri_dir = ((j)%2 == 0) == (i<invert_threshold)
        file_name = f'{count:04d}'
        count+=1

        if tri_dir:
            tri_copy = copy.deepcopy(tri_left["elements"][0])
        else:
            tri_copy = copy.deepcopy(tri_right["elements"][0])
        
        tri_from = tri_copy["from"]
        tri_to = tri_copy["to"]

        tri_scale = [
            tri_to[0] - tri_from[0],
            (tri_to[1] - tri_from[1])*vert_scale,
            tri_to[2] - tri_from[2]
        ]
        tri_to[0] = tri_to[0] + i*tri_scale[0] + 0.01
        tri_to[1] = tri_to[1] + j*tri_scale[1] - add_height*tri_scale[1]*0.5 + 0.01
        tri_to[2] = tri_to[2]

        tri_from[0] = tri_from[0] + i*tri_scale[0] - 0.01
        tri_from[1] = tri_from[1] + j*tri_scale[1] - add_height*tri_scale[1]*0.5 - 0.01
        tri_from[2] = tri_from[2]
        
        clampArray(tri_from)
        clampArray(tri_to)

        data = {
                "parent": "bigstone_sandbox:item/display_base",
                "elements": [tri_copy]
            }

        with open(os.path.join(output_dir, f"{file_name}.json"), 'w') as f:
            json.dump(data, f, indent=2)

print(f"Generated {count} JSON files in {output_dir}\n")
