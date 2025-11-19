import json

def sample_high_res_index(x, y, z):
    """Return the voxel index in the 16x16x16 high-res grid 
       that corresponds to the 'top corner' of the 2x2x2 block."""
    hx = x * 2 + 1
    hy = y * 2 + 1
    hz = z * 2 + 1
    return hx + hy * 16 + hz * 256

neighbourCheck = [
    [-1,0,0],[1,0,0],
    [0,-1,0],[0,1,0],
    [0,0,-1],[0,0,1]
]
def generateVoxObject(file_dir, width, neighbours_to_check = neighbourCheck, downsample=False):
    voxel = []
    height = width
    depth = width
    target = width * height * depth

    # 3D offsets for neighbor checks
    off_x = 1
    off_y = width
    off_z = width * height

    for i in range(target):
        index_str = f"{i:x}"

        # Convert 1D → 3D
        x = i % width
        y = (i // width) % height
        z = i // (width * height)

        # Compute neighbor indices
        neighbours = [
            i + (neigh[0]*off_x) + (neigh[1]*off_y) + (neigh[2]*off_z) for neigh in neighbours_to_check
        ]

        # Edge detection
        is_edge = False
        for dx, dy, dz in neighbours_to_check:
            nx = x + dx
            ny = y + dy
            nz = z + dz
            if nx < 0 or nx >= width or ny < 0 or ny >= height or nz < 0 or nz >= depth:
                is_edge = True
                break

        # Determine correct tint index
        if downsample:
            # sample the 2x2x2 block corner in the full 16³ grid
            tint_index = sample_high_res_index(x, y, z)
        else:
            # normal: tint is just the voxel index
            tint_index = i

        voxel_cube = {
            "type": "minecraft:model",
            "model": f"bigstone_sandbox:item/{file_dir}/{index_str}",
            "tints": [
                {
                    "type": "minecraft:custom_model_data",
                    "default": 16777215,
                    "index": tint_index
                }
            ]
        }

        voxel_tree = {"type": "minecraft:empty"}

        # Only add culling if not on the outside
        if not is_edge and all(0 <= n < target for n in neighbours):
            for j in neighbours:
                node_tint_index = (
                    sample_high_res_index(j % width, (j // width) % height, j // (width * height))
                    if downsample else j
                )

                voxel_node = {
                    "type": "minecraft:condition",
                    "property": "minecraft:custom_model_data",
                    "index": node_tint_index,
                    "on_true": voxel_tree,
                    "on_false": voxel_cube
                }
                voxel_tree = voxel_node

        else:
            voxel_tree = voxel_cube

        voxel_group = {
            "type": "minecraft:condition",
            "property": "minecraft:custom_model_data",
            "index": tint_index,
            "on_true": voxel_tree,
            "on_false": {"type": "minecraft:empty"}
        }

        voxel.append(voxel_group)

    return {
        "type": "minecraft:composite",
        "models": voxel
    }

# Generate models

voxel_output = generateVoxObject(
    "component_3d_item",
    16,
    downsample=False
)

voxel_output_half_res = generateVoxObject(
    "component_3d_item_half_res",
    8,
    downsample=True      # real 2x2x2 sampling!
)
neighbourCheck_gui = [
    [-1,0,0],
    [0,1,0],
    [0,0,1]
]
voxel_output_gui = generateVoxObject(
    "component_3d_item_gui",
    16,
    neighbours_to_check=neighbourCheck_gui,
    downsample=False
)
neighbourCheck_fp = [
    [1,0,0],
    [0,1,0],
    [0,0,-1]
]
voxel_output_fp = generateVoxObject(
    "component_3d_item_fp",
    16,
    neighbours_to_check=neighbourCheck_fp,
    downsample=False
)
neighbourCheck_fp_offhand = [
    [-1,0,0],
    [0,1,0],
    [0,0,-1]
]
voxel_output_fp_offhand = generateVoxObject(
    "component_3d_item_fp_offhand",
    16,
    neighbours_to_check=neighbourCheck_fp_offhand,
    downsample=False
)

# variables for dummy
n = 256  # change this — will generate 00..n entries
scale = 128

entries = []
entries_in_use = []
for i in range(n + 1):
    threshold = (scale / n) * i  # evenly spaced 0 → 32
    model_path = f"bigstone_sandbox:item/component_dummy_inner_cube/{i:02}"

    entries.append({
        "model": {
            "type": "model",
            "model": model_path,
            "tints": [
                {
                "type": "minecraft:constant",
                "value": [0.75,0.8,0.8]
                }
            ]
        },
        "threshold": round(threshold, 6)
    })

    entries_in_use.append({
        "model": {
            "type": "model",
            "model": model_path,
            "tints": [
                {
                "type": "minecraft:constant",
                "value": [0.1,0.9,1.0]
                }
            ]
        },
        "threshold": round(threshold, 6)
    })

model_dummy = {
                    "type": "composite",
                    "models": [
                        {
                            "type": "model",
                            "model": "bigstone_sandbox:item/display_dummy_container"
                        },
                        {
                            "type": "minecraft:range_dispatch",
                            "property": "minecraft:compass",
                            "scale": scale,
                            "target": "none",
                            "entries": entries,
                        }
                    ]
                }

model_dummy_in_use = {
                    "type": "composite",
                    "models": [
                        {
                            "type": "model",
                            "model": "bigstone_sandbox:item/display_dummy_container"
                        },
                        {
                            "type": "minecraft:range_dispatch",
                            "property": "minecraft:compass",
                            "scale": scale,
                            "target": "none",
                            "entries": entries_in_use,
                        }
                    ]
                }


display_context = {
        "type": "minecraft:select",
        "property": "minecraft:display_context",
        "cases": [
            {
                "when": ["fixed","head"],
                "model": voxel_output
            },
            {
                "when": ["gui"],
                "model": voxel_output_gui
            },
            {
                "when": ["firstperson_righthand"],
                "model": voxel_output_fp
            },
            {
                "when": ["firstperson_lefthand"],
                "model": voxel_output_fp_offhand
            }
        ],
        "fallback": voxel_output_half_res
    }

custom_display = {
    "type": "minecraft:condition",
    "property": "minecraft:has_component",
    "component": "custom_model_data",
    "on_true": display_context,
    "on_false": model_dummy
}

data_body = {
    "model": custom_display
}

with open("component_3d_item.json", "w") as f:
    json.dump(data_body, f, indent=4)
print("done")
