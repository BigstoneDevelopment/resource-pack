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


if __name__ == "__main__":

    edges_to_check = [(-1, 0, 0), (0, 1, 0), (0, 0, 1)]
    diagonal_vector = (1, -1, -1)
    dims = cube(16, 16, 16)

    voxel_list = generate_vox.diagonal_list(dims,edges_to_check,diagonal_vector)
    voxel_json = voxel_interpreter("component_3d_item_gui",voxel_list)
    print(json.dumps(voxel_json, indent=4))
    print("done!")
    #print(" ".join(map(str, res)))