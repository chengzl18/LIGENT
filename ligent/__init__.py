from ligent.server.server import serve, serve_fork, set_scenes_dir
from ligent.core.env import Environment
from ligent.utils import *
import argparse
import os


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("function", help="serve or play")

    parser.add_argument(
        "--time_scale",
        default=1.0,
        action="store",
        help="time scale to accelerate the game",
    )
    parser.add_argument(
        "--max_steps",
        default=0,
        action="store",
        help="max steps for one episode, 0 means infinite",
    )
    parser.add_argument(
        "--scenes",
        default="",
        action="store",
        help="user pre-defined scene files under a directory rather than instantly generated scene files",
    )
    parser.add_argument(
        "--env_path",
        default="",
        action="store",
        help="the executable file of the game client",
    )
    args = parser.parse_args()
    store_json(
        {
            "id": 0,
            "time_scale": args.time_scale,
            "max_steps": args.max_steps,
            "scenes": args.scenes,
            "buffer_file": os.path.join(os.getcwd(), "game_states.json"),
        },
        "env_config.json",
    )
    if args.function == "serve":
        serve()
    elif args.function == "play":
        serve_fork(args.env_path)
