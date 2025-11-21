import json

target = 16*16*16
voxel = []
#face_list = ["n","s","e","w","u","d"]
face_list = [
    {
        "face":"s",
        "checklist":[1],
        "is_edge":{
            "x":[15]
        }
    },
    {
        "face":"n",
        "checklist":[-1],
        "is_edge":{
            "x":[0]
        }
    },
    {
        "face":"w",
        "checklist":[-256],
        "is_edge":{
            "z":[0]
        }
    },
    {
        "face":"e",
        "checklist":[256],
        "is_edge":{
            "z":[15]
        }
    },
    {
        "face":"d",
        "checklist":[-16],
        "is_edge":{
            "y":[0]
        }
    },
    {
        "face":"u",
        "checklist":[16],
        "is_edge":{
            "y":[15]
        }
    }
]
for i in range(target):  # num
    index_str = f"{i:04d}"  # 0000, 0001
    for face in face_list:


        x = i % 16
        y = (i // 16) % 16
        z = i // 256

        neighbours = []
        for check in face["checklist"]:
            neighbours.append(i+check)
        
        is_edge = (
            any(x == key for key in face["is_edge"].get("x",[])) or
            any(y == key for key in face["is_edge"].get("y",[])) or
            any(z == key for key in face["is_edge"].get("z",[]))
        )

        voxel_cube = {
            "type": "minecraft:model",
            "model": f"bigstone_sandbox:item/component_3d_item/{index_str}{face["face"]}",
            "tints": [
                {
                    "type": "minecraft:custom_model_data",
                    "default": 16777215,
                    "index": i
                }
            ]
        }
        voxel_tree = {
            "type": "minecraft:empty"
        }
        if not is_edge and all(0 <= n < target for n in neighbours):
            for j in neighbours:
                voxel_node = {
                    "type": "minecraft:condition",
                    "property": "minecraft:custom_model_data",
                    "index": j,
                    "on_true": voxel_tree,
                    "on_false": voxel_cube
                }
                voxel_tree = voxel_node
        else:
            voxel_tree = voxel_cube
        voxel_group = {
            "type": "minecraft:condition",
            "property": "minecraft:custom_model_data",
            "index": i,
            "on_true": voxel_tree,
            "on_false": {
                "type": "minecraft:empty"
            }
        }
        voxel.append(voxel_group)

voxel_output = {
    "type": "minecraft:composite",
    "models": voxel
}

data_body = {
    "model": voxel_output
}

with open("component_3d_item.json", "w") as f:
    json.dump(data_body, f, indent=4)
print("done")
