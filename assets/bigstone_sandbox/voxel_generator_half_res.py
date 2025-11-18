import os
import json
import sys
import copy
import shutil
import math

script_dir = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(script_dir, 'models', 'item', 'component_3d_item_half_res')
try:
    shutil.rmtree(output_dir)
    print("folder cleared")
except:
    print("empty folder, detect continuing")
os.makedirs(output_dir, exist_ok=True)

def clampArray(ar):
    ar[0] = round(ar[0],2)
    ar[1] = round(ar[1],2)
    ar[2] = round(ar[2],2)

    ar[0] = min(max(ar[0],-16),32)
    ar[1] = min(max(ar[1],-16),32)
    ar[2] = min(max(ar[2],-16),32)

def offsetUV(uv,x,y):
    uv[0]+=x
    uv[1]+=y
    uv[2]+=x
    uv[3]+=y

width_count = 8
height_count = 8
depth_count = 8
offset_x = 0
offset_y = 0
offset_z = 0


def generateFace(ref, name):
    count = 0

    #voxel face_1
    voxel_face_ref = os.path.join(script_dir, 'models', 'item', ref)
    print("ref:"+voxel_face_ref+"\n")
    if not os.path.isfile(voxel_face_ref):
        sys.exit("Error, can't find script")
    print("found display reference 1 in "+voxel_face_ref+"\n")

    with open(voxel_face_ref, 'r') as f1:
        voxel_face = json.load(f1)

    for i in range(width_count):
        for j in range(height_count):
            for k in range(depth_count):
                file_name = '{0:x}'.format(count)
                count+=1
                
                _copy = copy.deepcopy(voxel_face["elements"][0])

                _from = _copy["from"]
                _to = _copy["to"]

                _faces = _copy["faces"]

                _north_uv = _faces["north"]["uv"]
                _south_uv = _faces["south"]["uv"]
                _east_uv = _faces["east"]["uv"]
                _west_uv = _faces["west"]["uv"]
                _up_uv = _faces["up"]["uv"]
                _down_uv = _faces["down"]["uv"]

                offsetUV(_north_uv,15-i,15-j)
                offsetUV(_south_uv,i,15-j)
                offsetUV(_east_uv,15-k,15-j)
                offsetUV(_west_uv,k,15-j)
                offsetUV(_up_uv,i,k)
                offsetUV(_down_uv,15-i,k)

                _scale = [
                    2,
                    2,
                    2
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
                        "parent": "bigstone_sandbox:item/v",
                        "elements": [_copy]
                    }

                with open(os.path.join(output_dir, f"{file_name}{name}.json"), 'w') as f:
                    json.dump(data, f, indent=2)
    print(f"Generated {count} JSON files for {name} in {output_dir}\n")
    
voxel_face_files = [
    {"file":"voxel_template_half_res.json", "name":""},
]
for face in voxel_face_files:
    generateFace(face["file"],face["name"])
print("done!")
