import os
import json
import sys
import copy
import math

script_dir = os.path.dirname(os.path.abspath(__file__))

#voxel face
voxel_face_ref = os.path.join(script_dir, 'models', 'item', "voxel_face.json")
print("ref:"+voxel_face_ref+"\n")
if not os.path.isfile(voxel_face_ref):
    sys.exit("Error, can't find script")
print("found display reference 1 in "+voxel_face_ref+"\n")

with open(voxel_face_ref, 'r') as f1:
    voxel_face = json.load(f1)

output_dir = os.path.join(script_dir, 'models', 'item', 'component_3d_item')
os.makedirs(output_dir, exist_ok=True)

def clampArray(ar):
    ar[0] = round(ar[0],2)
    ar[1] = round(ar[1],2)
    ar[2] = round(ar[2],2)

    ar[0] = min(max(ar[0],-16),32)
    ar[1] = min(max(ar[1],-16),32)
    ar[2] = min(max(ar[2],-16),32)

count = 0
width_count = 16
height_count = 16
depth_count = 16
offset_x = 0
offset_y = 0
offset_z = 0

for i in range(width_count):
    for j in range(height_count):
        for k in range(depth_count):
            file_name = f'{count:04d}'
            count+=1
            
            _copy = copy.deepcopy(voxel_face["elements"][0])
            _from = _copy["from"]
            _to = _copy["to"]

            _scale = [
                _to[0] - _from[0],
                _to[1] - _from[1],
                _to[2] - _from[2]
            ]

            _to[0] = _to[0] + i*_scale[0] + offset_x
            _to[1] = _to[1] + j*_scale[1] + offset_y
            _to[2] = _to[2] + k*_scale[1] + offset_z

            _from[0] = _from[0] + i*_scale[0] - offset_x
            _from[1] = _from[1] + j*_scale[1] - offset_y
            _from[2] = _from[2] + k*_scale[1] - offset_z
            
            clampArray(_from)
            clampArray(_to)

            data = {
                    "parent": "bigstone_sandbox:item/display_base_voxel",
                    "elements": [_copy]
                }

            with open(os.path.join(output_dir, f"{file_name}.json"), 'w') as f:
                json.dump(data, f, indent=2)

print(f"Generated {count} JSON files in {output_dir}\n")


