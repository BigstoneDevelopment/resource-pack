import json
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))

voxel_face_files = [
    {"file":"voxel_face_north.json", "name":"n"},
    {"file":"voxel_face_south.json", "name":"s"},
    {"file":"voxel_face_east.json", "name":"e"},
    {"file":"voxel_face_west.json", "name":"w"},
    {"file":"voxel_face_up.json", "name":"u"},
    {"file":"voxel_face_down.json", "name":"d"}
]
voxel_data = []
#voxel face_1
def append_voxel_file(ref,name):
    voxel_face_ref = os.path.join(script_dir, ref)
    print("ref:"+voxel_face_ref+"\n")
    if not os.path.isfile(voxel_face_ref):
        sys.exit("Error, can't find script")
    print("found display reference 1 in "+voxel_face_ref+"\n")

    with open(voxel_face_ref, 'r') as f1:
        voxel_face = json.load(f1)
    #print(voxel_face["elements"][0]["faces"])
    voxel_data.append({
        "data":voxel_face["elements"][0]["faces"],
        "name":name
        })

for face in voxel_face_files:
    append_voxel_file(face["file"],face["name"])

file_output_unfiltered = []
for i in range(2**len(voxel_data)):
    voxel_file = []
    name_list = []
    for j in range(len(voxel_data)):
        if (i >> j) & 1:
            voxel_file.append(voxel_data[j]["data"])
            name_list.append(voxel_data[j]["name"])
    if (voxel_file):
        file_output_unfiltered.append({
        "output":voxel_file,
        "name_list":name_list
    })

def merge_faces(face_list):
    merged = {}
    for f in face_list:
        merged.update(f)  # later faces overwrite earlier ones
    return merged

output_dir = os.path.join(script_dir, "generated")
os.makedirs(output_dir, exist_ok=True)

def save_voxel_file(name, faces_dict):
    output_path = os.path.join(output_dir, f"{name}.json")

    obj = {
        "elements": [
            {
                "from": [0, 0, 0],
		        "to": [1, 1, 1],
                "faces": faces_dict
            }
        ]
    }

    with open(output_path, "w") as f:
        json.dump(obj, f, indent=4)

    print("Generated:", output_path)

for file_to_save in file_output_unfiltered:
    merged_faces = merge_faces(file_to_save["output"])
    save_voxel_file(''.join(file_to_save["name_list"]), merged_faces)
#print(voxel_data)