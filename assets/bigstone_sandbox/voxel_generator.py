import os
import json
import sys
import copy

n = 1536

script_dir = os.path.dirname(os.path.abspath(__file__))
item_display_script_ref = os.path.join(script_dir, 'models', 'item', "item_display_script_ref.json")
print("ref:"+item_display_script_ref+"\n")
if not os.path.isfile(item_display_script_ref):
    sys.exit("Error, can't find script")
print("found display reference in "+item_display_script_ref+"\n")

with open(item_display_script_ref, 'r') as f:
    item_display_base = json.load(f)

output_dir = os.path.join(script_dir, 'models', 'item', 'component_item')
os.makedirs(output_dir, exist_ok=True)

for i in range(n):
    file_name = f'{i:04d}'
    parent_index = "tri_left" if (i % 2 == 0) else "tri_right"

    data = {
        "parent": f"bigstone_sandbox:item/{parent_index}"
    }

    # deep copy so modifying doesn't affect the original
    display_copy = copy.deepcopy(item_display_base["display"])

    # vertical movement
    for section, props in display_copy.items():
        if "translation" in props and "scale" in props:
            props["translation"][1] += props["scale"][1] * 0.625*((i % 31)-(i // 31))
            props["translation"][1] = max(min(round(props["translation"][1],2), 80), -80)
            props["translation"][0] -= props["scale"][0]*((i//31))

    data["display"] = display_copy
    data["gui_light"] = item_display_base.get("gui_light")

    file_path = os.path.join(output_dir, f"{file_name}.json")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

print(f"Generated {n} JSON files in {output_dir}\n")
