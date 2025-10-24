import json

output = {
    "model": {
        "type": "minecraft:composite",
        "models": []
    }
}

for i in range(1535):  # 0 → 1536 inclusive
    index_str = f"{i:04d}"  # 0000, 0001, ..., 1536
    output["model"]["models"].append({
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

with open("component_item.json", "w") as f:
    json.dump(output, f, indent=2)

print("Generated component_item.json")
