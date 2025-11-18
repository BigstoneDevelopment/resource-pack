import json

target = 16*16*16
voxel = []
for i in range(target):  # num
    index_str = f"{i:04d}"  # 0000, 0001,

    x = i % 16
    y = (i // 16) % 16
    z = i // 256

    neighbours = [
        i - 1, i + 1,
        i - 16, i + 16,
        i - 256, i + 256
    ]

    is_edge = (
        x == 0 or x == 15 or
        y == 0 or y == 15 or
        z == 0 or z == 15
    )

    checklist = [i-1,i+1,i+16,i-16,i+16*2,i-16*16]

    voxel_cube = {
        "type": "minecraft:model",
        "model": f"bigstone_sandbox:item/component_3d_item/{index_str}",
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
