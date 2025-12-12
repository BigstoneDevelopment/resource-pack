#object instance that holds basic attributes of a voxel cube
import json
from typing import Iterable, List, Sequence, Tuple, Dict, Any

class cube:
    def __init__(self,width: int,height: int,depth: int):
        if width <= 0 or height <= 0 or depth <= 0:
            raise ValueError("width, height and depth must be positive integers")
        self.width = width
        self.height = height
        self.depth = depth
    
    def voxel_count(self) -> int:
        return self.width*self.height*self.depth
    
    #check if value is within range of the stated dimensions
    def is_inbound(self,x: int,y: int,z: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth

    def index_to_coord(self, index: int) -> Tuple[int, int, int]:
        if not (0 <= index < self.voxel_count()):
            raise IndexError(f"index {index} out of range for cube with {self.voxel_count()} voxels")
        x = index % self.width
        y = (index // self.width) % self.height
        z = index // (self.width * self.height)
        return x, y, z
    
    def coord_to_index(self, x: int, y: int, z: int) -> int:
        if not self.is_inbound(x, y, z):
            raise IndexError(f"coordinate {(x,y,z)} out of bounds")
        return x + y * self.width + z * self.width * self.height

    #return a list of only voxel dimensions
    def voxel_edges(self, edges_to_check: Iterable[Sequence[int]]) -> List[int]:
        edges_to_check = list(edges_to_check)
        voxel_edge_list: List[int]  = []

        #detect edges
        def is_edge(input_voxel,edges_to_check):
            x, y, z = self.index_to_coord(input_voxel)

            is_edge = False
            for dx, dy, dz in edges_to_check:
                nx = x + dx
                ny = y + dy
                nz = z + dz
                if not self.is_inbound(nx, ny, nz):
                    is_edge = True
                    break
            return is_edge
        
        for i in range(self.voxel_count()):
            #index = f"{i:x}"
            if is_edge(i,edges_to_check):
                voxel_edge_list.append(i)
        return voxel_edge_list
#voxel generation code
class generate_vox:
    @staticmethod
    def diagonal(dimensions: cube, voxel_start_pos: int, diagonal_to_propagate: Sequence[int]):

        if len(diagonal_to_propagate) != 3:
            raise ValueError("diagonal_to_propagate must be length 3 (dx,dy,dz)")
        dx, dy, dz = map(int, diagonal_to_propagate)

        # Convert 1D → 3D coordinates
        x, y, z = dimensions.index_to_coord(int(voxel_start_pos))
        voxel_diagonal_list: List[int] = []

        if dx == 0 and dy == 0 and dz == 0:
            raise ValueError("diagonal_to_propagate cannot be (0,0,0)")
        
        # Traverse along the diagonal until out of bounds
        while dimensions.is_inbound(x,y,z):
            # Convert 3D → 1D index and store
            index_output = dimensions.coord_to_index(x,y,z)
            voxel_diagonal_list.append(index_output)

            # Move along diagonal
            x += dx
            y += dy
            z += dz

        return voxel_diagonal_list
    
    @staticmethod
    def diagonal_list(dimensions: cube,edges_to_check: Iterable[Sequence[int]],diagonal_vector: Sequence[int])-> Tuple[List[List[int]], List[int]]:
        voxel_check = []
        voxel_list = []
        for n in dimensions.voxel_edges(edges_to_check):
            diagonal_list = generate_vox.diagonal(dimensions,n,diagonal_vector)
            voxel_list.append(diagonal_list)
            for m in diagonal_list:
                if not(m in voxel_check):
                    voxel_check.append(m)
                else:
                    print(f"{m} is a duplicate")
                    break
            else:
                continue
            break
        return voxel_list
#voxel processing code
class process_vox:
    @staticmethod
    def return_neighbours(voxel: int, dimensions: cube, neighbours_to_check: Iterable[Sequence[int]] = None,voxel_list: List = None) -> List[int]:

        if neighbours_to_check is None:
            neighbours_to_check = []
            
        valid_neighbours = []
        # Convert 1D → 3D coordinates
        x, y, z = dimensions.index_to_coord(int(voxel))

        for dx, dy, dz in neighbours_to_check:
            nx = x + dx
            ny = y + dy
            nz = z + dz

            # Bounds check
            if dimensions.is_inbound(nx,ny,nz):
                n_index = dimensions.coord_to_index(nx, ny, nz)
                valid_neighbours.append(n_index)
        
        if voxel_list is None:
            return valid_neighbours
        else:
            return valid_neighbours in voxel_list

#json interpreter
class vox_json:
    @staticmethod
    def str_index(index_str: int) -> str:
        return f"{index_str:x}"
    @staticmethod
    def vox_model(file_dir: str, index: int, default_tint: int = 16777215) -> Dict[str, Any]:
        file_name = vox_json.str_index(index)
        return {
            "type": "minecraft:model",
            "model": f"bigstone_sandbox:item/{file_dir}/{file_name}",
            "tints": [
                {
                    "type": "minecraft:custom_model_data",
                    "default": default_tint,
                    "index": index
                }
            ]
        }
    @staticmethod
    def composite(json_list):
        return {
            "type": "minecraft:composite",
            "models": json_list
        }
    @staticmethod
    def model(json: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "model": json
        }
    @staticmethod
    def index_condition(index: int,on_true: Dict[str, Any] = None, on_false: Dict[str, Any] = None)-> Dict[str, Any]:
        empty = {"type": "minecraft:empty"}
        if on_true is None:
            on_true = empty
        if on_false is None:
            on_false = empty
            
        return {
                "type": "minecraft:condition",
                "property": "minecraft:custom_model_data",
                "index": index,
                "on_true": on_true,
                "on_false": on_false
            }
    @staticmethod
    def simple_vox_chain(json_list: List[Dict[str, Any]]) -> Dict[str, Any]:

        if not json_list:
            return {"type": "minecraft:empty"}
        
        empty = {"type": "minecraft:empty"}
        #reverse list
        list_to_sort = list(reversed(json_list))
        voxel_tree = empty

        for model in list_to_sort:
            #why not some extra checks
            try:
                index = model["tints"][0]["index"]
            except Exception as e:
                raise KeyError("each model must have 'tints' with an index") from e
            
            #assign voxel group
            voxel_group = {
                "type": "minecraft:condition",
                "property": "minecraft:custom_model_data",
                "index": index,
                "on_true": model,
                "on_false": voxel_tree
            }
            voxel_tree = voxel_group
        return voxel_tree

def voxel_interpreter(file_dir: str, voxel_list: Sequence[Sequence[int]]) -> Dict[str, Any]:
    voxel_chain_list = []
    for voxel_group in voxel_list:
        voxel_temp_group = []
        #post process 1
        for voxel in voxel_group:
            voxel_temp_group.append(vox_json.vox_model(file_dir,voxel))
        #process 2
        voxel_chain_list.append(vox_json.simple_vox_chain(voxel_temp_group))
    return vox_json.composite(voxel_chain_list)


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
def generateVoxObject(file, width, neighbours_to_check = neighbourCheck,edges_to_check = [], downsample=False):
    voxel = []
    if not edges_to_check:
        edges_to_check = neighbours_to_check

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

        default_tint = 16777215

        if isinstance(file, list):
            list_pos = min(x, len(file) - 1)
            entry = file[list_pos]

            if isinstance(entry, dict):
                file_dir = entry["file"]
                neighbours_to_check = entry.get("neighbours_to_check", None)
            else:
                file_dir = entry
            # debug colour if last element
            #if list_pos == len(file) - 1:
            #    default_tint = 16718362
        else:
            # file is a single string
            file_dir = file
        # Compute neighbor indices
        neighbours = [
            i + (neigh[0]*off_x) + (neigh[1]*off_y) + (neigh[2]*off_z) for neigh in neighbours_to_check
        ]

        # Edge detection
        is_edge = False
        for dx, dy, dz in edges_to_check:
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
                    "default": default_tint,
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
#neighbourCheck_gui = [
#    [-1,0,0],
#    [0,1,0],
#    [0,0,1]
#]
#voxel_output_gui = generateVoxObject(
#    "component_3d_item_gui",
#    16,
#    neighbours_to_check=neighbourCheck_gui,
#    downsample=False
#)
neighbourCheck_fp = [
    [1,0,0],
    [0,1,0],
    [0,0,-1]
]
edgesCheck_fp = [
    [0,1,0]
]

neighbourCheck_fp_offhand = [
    [-1,0,0],
    [0,1,0],
    [0,0,-1]
]
voxel_output_fp = generateVoxObject(
    [
        "component_3d_item_fp",
        "component_3d_item_fp",
        "component_3d_item_fp",
        "component_3d_item_fp",
        "component_3d_item_fp",
        "component_3d_item_fp",
        "component_3d_item_fp",
        "component_3d_item_fp",
        "component_3d_item_fp",
        "component_3d_item_fp",
        "component_3d_item_fp",
        "component_3d_item_fp",
        "component_3d_item_fp",
        {
            "file":"component_3d_item_fp_offhand",
            "neighbours_to_check": neighbourCheck_fp_offhand
        },
    ],
    16,
    neighbours_to_check=neighbourCheck_fp,
    edges_to_check=edgesCheck_fp,
    downsample=False
)
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

if __name__ == "__main__":

    edges_to_check = [(-1, 0, 0), (0, 1, 0), (0, 0, 1)]
    diagonal_vector = (1, -1, -1)
    dims = cube(16, 16, 16)

    voxel_list = generate_vox.diagonal_list(dims,edges_to_check,diagonal_vector)
    voxel_json_gui = voxel_interpreter("component_3d_item_gui",voxel_list)


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
                "model": voxel_json_gui
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

    data_body = vox_json.model(custom_display)
    with open("component_item.json", "w") as f:
        #json.dump(data_body, f, separators=(',', ':'))
        json.dump(data_body, f, indent=1)
    print("done")
    #print(json.dumps(voxel_json, indent=4))
    #print("done!")
    #print(" ".join(map(str, res)))