import os
import json
import sys
import copy

n = 1535

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

# --- Dynamic growing columns ---
base_height = 31
col_height = base_height           # current column height
col_index = 0                      # which column we're in
inv_col_index = 0
next_col_start = col_height       # i value at which we go to next column

for i in range(n):

    file_name = f'{i:04d}'

    display_copy = copy.deepcopy(item_display_base["display"])

    # vertical + horizontal movement using correct col_index now
    if i<(1536//2):
        # If we've reached or passed the boundary → open next column
        if i >= next_col_start:
            col_index += 1
            inv_col_index = col_index
            col_height = base_height + col_index * 2       # +2 per column
            next_col_start += col_height                   # grow the boundary forward

        parent_index = "tri_left" if ((i + inv_col_index) % 2 == 0) else "tri_right"

        data = {
            "parent": f"bigstone_sandbox:item/{parent_index}"
        }
        for section, props in display_copy.items():
            if "translation" in props and "scale" in props:
                # i % col_height only makes sense while still in this column
                local_i = i - (next_col_start - col_height)
                props["translation"][1] += props["scale"][1] * 0.625 * local_i-col_index/1.625
                props["translation"][1] = max(min(round(props["translation"][1], 2), 80), -80)

                props["translation"][0] -= props["scale"][0] * col_index
    else:
        if i >= next_col_start:
            col_index += 1
            inv_col_index -= 1
            col_height = base_height + inv_col_index * 2       # -2 per column
            next_col_start += col_height                   # grow the boundary forward

        parent_index = "tri_left" if ((i + inv_col_index) % 2 != 0) else "tri_right"

        data = {
            "parent": f"bigstone_sandbox:item/{parent_index}"
        }
        for section, props in display_copy.items():
            if "translation" in props and "scale" in props:
                # i % col_height only makes sense while still in this column
                local_i = i - (next_col_start - col_height)
                props["translation"][1] += props["scale"][1] * ((0.625 * local_i-inv_col_index/1.625)-0.625)
                props["translation"][1] = max(min(round(props["translation"][1], 2), 80), -80)

                props["translation"][0] -= props["scale"][0] * col_index

    data["display"] = display_copy
    data["gui_light"] = item_display_base.get("gui_light")

    with open(os.path.join(output_dir, f"{file_name}.json"), 'w') as f:
        json.dump(data, f, indent=2)

print(f"Generated {n} JSON files in {output_dir}\n")
