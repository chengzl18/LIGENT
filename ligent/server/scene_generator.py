from ligent.server.rect_placer import RectPlacer
from ligent.utils import *
import numpy as np
import json
import pkg_resources
from typing import Dict, Literal, Optional


prefabs = None  # all the prefabs info, including name, size and center offset (for Unity transform position)
interactableNames = []  # all the interactive object names, such as "Watermelon_01"
kinematicNames = []  # all the non-interactive object names, such as "KitchenTable_02"


def set_seed(seed: int = 42) -> None:
    np.random.seed(seed)


def load_prefabs() -> None:
    global prefabs, interactableNames, kinematicNames
    json_file_path = "addressables.json"  # Specify the relative path to the JSON file within the package
    json_file = pkg_resources.resource_filename(__name__, json_file_path)
    with open(json_file, "r", encoding="utf-8") as f:
        prefabs = json.load(f)["prefabs"]
        for prefab in prefabs:
            if prefab["isInteractable"]:
                interactableNames.append(prefab["name"])
            else:
                if prefab["name"] not in {"Floor_01", "WallFloor1_09"}:
                    kinematicNames.append(prefab["name"])
        prefabs = {prefab["name"]: prefab for prefab in prefabs}
    log("load prefabs info OK")


def generate_scene(object_counts: Dict[str, int]={}):
    # object_counts specifies a definite number for certain objects
    # For example, if you want to have only one instance of ChristmasTree_01 in the scene, you can set the object_counts as {"ChristmasTree_01": 1}.
    global prefabs, interactableNames, kinematicNames
    MAX = 7
    MID = MAX // 2
    floors = np.zeros(
        (MAX, MAX)
    )  # the spatial layout of the rooms. 1 for rooms and 0 for invalid spaces
    floors[MID][MID] = 1

    ### STEP 1: Create Rooms Randomly
    # Create the first room.
    # starting from the center point, expand in four directions to create the first room
    # top, down, left, right represents the expansion distance in each direction starting from the center point
    top, down, left, right = (
        np.random.randint(0, MID + 1),
        np.random.randint(0, MID + 1),
        np.random.randint(0, MID + 1),
        np.random.randint(0, MID + 1),
    )
    x0, x1, z0, z1 = MID - top, MID + down, MID - left, MID + right
    floors[x0 : x1 + 1, z0 : z1 + 1] = 1
    area0_range = (
        (x0 - MID) * 2.5 - 1.25,
        (x1 - MID) * 2.5 + 1.25,
        (z0 - MID) * 2.5 - 1.25,
        (z1 - MID) * 2.5 + 1.25,
    )
    area0 = (area0_range[1] - area0_range[0]) * (area0_range[3] - area0_range[2])

    # Create the second room.
    # Determine the position of the second room. Use absolute coordinates for all positions.
    # (x0, z0) (x1, z1) represents two corners of the second room.
    x0, z0 = np.random.randint(MID - top, MID + down + 1), np.random.randint(
        MID - left, MID + right + 1
    )
    x1, z1 = np.random.randint(0, MAX), np.random.randint(0, MAX)
    x0, x1, z0, z1 = min(x0, x1), max(x0, x1), min(z0, z1), max(z0, z1)
    floors[x0 : x1 + 1, z0 : z1 + 1] = 2
    area1_range = (
        (x0 - MID) * 2.5 - 1.25,
        (x1 - MID) * 2.5 + 1.25,
        (z0 - MID) * 2.5 - 1.25,
        (z1 - MID) * 2.5 + 1.25,
    )
    area1 = (area1_range[1] - area1_range[0]) * (area1_range[3] - area1_range[2])

    ### STEP 2: Create Floors and Walls
    # create rectangle placer to avoid object overlapping
    min_x, max_x = min(area0_range[0], area1_range[0]), max(
        area0_range[1], area1_range[1]
    )
    min_z, max_z = min(area0_range[2], area1_range[2]), max(
        area0_range[3], area1_range[3]
    )
    placer = RectPlacer((min_x, min_z, max_x, max_z))

    floor_instances = []
    # generate walls based on the 0-1 boundaries
    for i in range(MAX):
        for j in range(MAX):
            if floors[i][j] != 0:
                x, z = (i - MID) * 2.5, (j - MID) * 2.5
                floor_instances.append(
                    {
                        "prefab": "Floor_01",
                        "position": [x, 0, z],
                        "rotation": [0, 90, 0],
                        "scale": [1, 1, 1],
                    }
                )
            x_size, y_size, z_size = (
                prefabs["WallFloor1_09"]["size"]["x"],
                prefabs["WallFloor1_09"]["size"]["y"],
                prefabs["WallFloor1_09"]["size"]["z"],
            )
            # above is 0 and below is 1
            # the wall at the upper edge of the floor
            if (i - 1 < 0 or floors[i - 1][j] == 0) and floors[i][j] != 0:
                x, z = (i - MID) * 2.5 - 1.25, (j - MID) * 2.5
                bbox = (
                    x
                    - z_size
                    / 2,  # The wall is rotated 90 degrees. The sizes corresponding to z and x need to be swapped.
                    z - x_size / 2,
                    x + z_size / 2,
                    z + x_size / 2,
                )
                placer.insert("WallFloor1_09", bbox)
                floor_instances.append(
                    {
                        "prefab": "WallFloor1_09",
                        "position": [x, y_size / 2, z],
                        "rotation": [0, 90, 0],
                        "scale": [1, 1, 1],
                    }
                )
            # above is 1 and below is 0
            # the wall at the lower edge of the floor
            if (i + 1 >= MAX or floors[i + 1][j] == 0) and floors[i][j] != 0:
                x, z = (i - MID) * 2.5 + 1.25, (j - MID) * 2.5
                bbox = (x - z_size / 2, z - x_size / 2, x + z_size / 2, z + x_size / 2)
                placer.insert("WallFloor1_09", bbox)
                floor_instances.append(
                    {
                        "prefab": "WallFloor1_09",
                        "position": [x, y_size / 2, z],
                        "rotation": [0, 90, 0],
                        "scale": [1, 1, 1],
                    }
                )
            # left is 0 and right is 1
            # the wall at the left edge of the floor
            if (j - 1 < 0 or floors[i][j - 1] == 0) and floors[i][j] != 0:
                x, z = (i - MID) * 2.5, (j - MID) * 2.5 - 1.25
                bbox = (x - x_size / 2, z - z_size / 2, x + x_size / 2, z + z_size / 2)
                placer.insert("WallFloor1_09", bbox)
                floor_instances.append(
                    {
                        "prefab": "WallFloor1_09",
                        "position": [x, y_size / 2, z],
                        "rotation": [0, 0, 0],
                        "scale": [1, 1, 1],
                    }
                )
            # left is 1 and right is 0
            # the wall at the right edge of the floor
            if (j + 1 >= MAX or floors[i][j + 1] == 0) and floors[i][j] != 0:
                x, z = (i - MID) * 2.5, (j - MID) * 2.5 + 1.25
                bbox = (x - x_size / 2, z - z_size / 2, x + x_size / 2, z + z_size / 2)
                placer.insert("WallFloor1_09", bbox)
                floor_instances.append(
                    {
                        "prefab": "WallFloor1_09",
                        "position": [x, y_size / 2, z],
                        "rotation": [0, 0, 0],
                        "scale": [1, 1, 1],
                    }
                )

    # the random positions for characters and objects should be within the valid area
    def random_xz_in_area():
        areas = np.array([area0, area1])
        areas = areas / areas.sum()
        area_range = [area0_range, area1_range][
            int(np.random.choice([0, 1], 1, p=areas))
        ]
        return np.random.uniform(area_range[0], area_range[1]), np.random.uniform(
            area_range[2], area_range[3]
        )

    def random_xz_in_area_inner(
        eps,
    ):  # To prevent being positioned in the wall and getting pushed out by collision detection.
        area0_range_inner = (
            area0_range[0] + eps,
            area0_range[1] - eps,
            area0_range[2] + eps,
            area0_range[3] - eps,
        )
        area1_range_inner = (
            area1_range[0] + eps,
            area1_range[1] - eps,
            area1_range[2] + eps,
            area1_range[3] - eps,
        )
        areas = np.array([area0, area1])
        areas = areas / areas.sum()
        area_range = [area0_range_inner, area1_range_inner][
            int(np.random.choice([0, 1], 1, p=areas))
        ]
        return np.random.uniform(area_range[0], area_range[1]), np.random.uniform(
            area_range[2], area_range[3]
        )

    ### STEP 3: Randomly place the player and playmate (AI agent)
    # place the player
    while True:
        x, z = random_xz_in_area_inner(eps=0.5)
        x_size, z_size = 1, 1
        player = {
            "prefab": "",
            "position": [
                x,
                0.05,
                z,
            ],  # TODO: obtain the precise centerOffset of the character. calculate y based on it.
            "rotation": [0, np.random.uniform(0, 360), 0],
            "scale": [1, 1, 1],
            "parent": -1,
        }
        ok = placer.place_rectangle(
            "player",
            bbox=(x - x_size / 2, z - z_size / 2, x + x_size / 2, z + z_size / 2),
        )
        if ok:
            break
    # place the playmate
    while True:
        x, z = random_xz_in_area_inner(eps=0.5)
        x_size, z_size = 1, 1
        playmate = {
            "prefab": "",
            "position": [x, 0.05, z],
            "rotation": [0, np.random.uniform(0, 360), 0],
            "scale": [1, 1, 1],
            "parent": -1,
        }
        ok = placer.place_rectangle(
            "playmate",
            bbox=(x - x_size / 2, z - z_size / 2, x + x_size / 2, z + z_size / 2),
        )
        if ok:
            break

    ### STEP 4: Create Objects Randomly
    object_instances = []
    max_nums = {
        name: 10 for name in kinematicNames
    }  # Limit the maximum number of each type of object.

    def put_once(_name, _placer: RectPlacer, parent_idx, rand_method: Literal["eps", "fit"], return_bbox=False):
        # Put _name in _placer on parent_idx

        _x_size, _y_size, _z_size = (
            prefabs[_name]["size"]["x"],
            prefabs[_name]["size"]["y"],
            prefabs[_name]["size"]["z"],
        )
        if rand_method=="eps": # put at a fixed distance from the edge of the area
            if _name in kinematicNames:
                _x, _z = random_xz_in_area_inner(eps=0.05)
            else:
                _x, _z = random_xz_in_area_inner(eps=0.2) # Avoid generating small objects close to the wall
        elif rand_method=="fit": # put exactly inside the area
            _bbox = _placer.bbox
            _x_min, _x_max, _z_min, _z_max = _bbox[0], _bbox[2], _bbox[1], _bbox[3]
            try:
                # eps will be dynamically determined based on the size of the object
                # TODO: all previous eps related logic follow this approach.
                _x, _z = np.random.uniform(
                    _x_min + _x_size / 2, _x_max - _x_size / 2
                ), np.random.uniform(_z_min + _z_size / 2, _z_max - _z_size / 2)
            except:  # the right range may be smaller than the left range. unable to place.
                return False
        _bbox = (_x - _x_size / 2, _z - _z_size / 2, _x + _x_size / 2, _z + _z_size / 2)
        ok = _placer.place_rectangle(_name, bbox=_bbox)
        if parent_idx == 0:
            _y_base = 0 + prefabs["Floor_01"]["size"]["y"] / 2   # center + size / 2
        else:
            parent_info = object_instances[parent_idx-len(floor_instances)]
            _y_base = parent_info["position"][1] + prefabs[parent_info["prefab"]]["size"]["y"]/2
        if ok:
            _y = _y_base + _y_size / 2
            object_instances.append(
                {
                    "prefab": name,
                    "position": [_x, _y, _z],
                    "rotation": [0, 0, 0],
                    "scale": [1, 1, 1],
                    "parent": parent_idx, # 0 represents the floor
                }
            )
        if return_bbox:
            return ok, _bbox
        return ok
    
    def put_one(_name, _placer: RectPlacer, parent_idx, rand_method: Literal["eps", "fit"], return_bbox=False):
        ok = False
        while not ok:
            ok, _bbox = put_once(_name, _placer, parent_idx, rand_method, True)
        if return_bbox:
            return True, _bbox
        return True
    
    # generate objects with a specified number
    for name in object_counts:
        for i in range(object_counts[name]):
            put_one(name, placer, 0, "eps")
    random_kinematic_names = [name for name in kinematicNames if name not in object_counts]
    random_interactable_names = [name for name in interactableNames if name not in object_counts]

    # create non-interactive objects
    for i in range(10):
        name = np.random.choice(random_kinematic_names)
        if max_nums[name] == 0:
            continue
        max_nums[name] -= 1
        ok, bbox = put_once(name, placer, 0, "eps", return_bbox=True)
        if ok:
            parent_idx = len(floor_instances) + len(object_instances) - 1
            # Generate some objects on this non-interactive object (such as a table).
            # bbox represent the range of the tabletop
            subplacer = RectPlacer(bbox=bbox)
            sub_object_nums = 10 if sum([n in name for n in {"Table", "Catpet"}]) else 0
            for i in range(sub_object_nums):
                name = np.random.choice(random_interactable_names)
                put_once(name, subplacer, parent_idx, "fit")

    # create interactive objects
    for i in range(20):
        name = np.random.choice(random_interactable_names)
        put_once(name, placer, 0, "eps")

    ### STEP 5: Adjust Positions for Unity GameObject
    # Convert all the positions (the center of the mesh bounding box) to positions of Unity GameObject transform
    # They are not equal because position of a GameObject also depends on the relative center offset of the mesh within the prefab
    instances = floor_instances + object_instances
    for inst in instances:
        pos, offset = inst["position"], prefabs[inst["prefab"]]["centerOffset"]
        # gameobject position to center position use '+ offset'
        # center position to gameobject position use '- offset';
        inst["position"] = [
            pos[0] - offset["x"],
            pos[1] - offset["y"],
            pos[2] - offset["z"],
        ]

    height = max(12, (max_z - min_z) * 1 + 2)
    center = [(min_x + max_x) / 2, height, (min_z + max_z) / 2]
    infos = {
        "prompt": "",
        "instances": instances,
        "player": player,
        "playmate": playmate,
        "center": center,
    }
    with open("last_scene.json", "w", encoding="utf-8") as f:
        json.dump(infos, f, ensure_ascii=False, indent=4)
    return infos


if __name__ == "__main__":
    import os
    load_prefabs()
    os.makedirs("custom_scenes", exist_ok=True)

    for i in range(5):
        scene = generate_scene()
        store_json(scene, f'custom_scenes/{i}.json')
