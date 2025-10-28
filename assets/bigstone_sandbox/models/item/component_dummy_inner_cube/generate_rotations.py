import json
import math

n = 256  # how many files? 36 → rotates 10° per file. Change as needed.
m = 2
for i in range(n + 1):
    angle0 = ((360) / (n + 1)) * i   # full loop
    angle0 = round(angle0, 3)       # cleaner output

    angle1 = ((360) / (n + 1)) * i   # full loop
    angle1 = round(angle0, 3)       # cleaner output

    data = {
        "parent": "bigstone_sandbox:item/display_dummy_inner_cube",
        "display": {
            "thirdperson_righthand": {
                "rotation": [angle1, angle0, 0],
                "translation": [0, 2.5, 0],
                "scale": [0.375, 0.375, 0.375]
            },
            "thirdperson_lefthand": {
                "rotation": [angle1, angle0, 0],
                "translation": [0, 2.5, 0],
                "scale": [0.375, 0.375, 0.375]
            },
            "firstperson_righthand": {
                "rotation": [angle1, angle0, 0],
                "scale": [0.4, 0.4, 0.4]
            },
            "firstperson_lefthand": {
                "rotation": [angle1, angle0, 0],
                "scale": [0.4, 0.4, 0.4]
            },
            "ground": {
                "rotation": [angle1, angle0, 0],
                "translation": [0, 3, 0],
                "scale": [0.25, 0.25, 0.25]
            },
            "gui": {
                "rotation": [angle1, angle0, 0],
                "scale": [0.625, 0.625, 0.625]
            },
            "fixed": {
                "rotation": [angle1, angle0, 0],
                "scale": [0.5, 0.5, 0.5]
            }
        }
    }

    filename = f"{i:02}.json"  # 00.json, 01.json, 02.json …
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Created {filename} with rotation {angle0}°")