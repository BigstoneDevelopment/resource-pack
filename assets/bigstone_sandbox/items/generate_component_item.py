import json

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

voxel_tri = []
for i in range(1536):  # 0 → 1536 inclusive
    index_str = f"{i:04d}"  # 0000, 0001, ..., 1536
    voxel_tri.append({
        "type": "minecraft:condition",
        "property": "minecraft:custom_model_data",
        "index": i,
        "on_true": {
            "type": "minecraft:model",
            "model": f"bigstone_sandbox:item/component_item/{index_str}",
            "tints": [
                {
                    "type": "minecraft:custom_model_data",
                    "default": 16777215,
                    "index": i
                }
            ]
        },
        "on_false": {
            "type": "minecraft:empty"
        }
    })

voxel_output = {
    "type": "minecraft:composite",
    "models": voxel_tri
}


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
                "when": ["gui","firstperson_righthand","firstperson_lefthand"],
                "model": voxel_output
            }
        ],
        "fallback": model_dummy_in_use
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

with open("component_item.json", "w") as f:
    json.dump(data_body, f, separators=(',', ':'))

print(f"Generated component_item.json with {n+1} entries.")
