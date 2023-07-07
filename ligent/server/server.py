from ligent.server.scene_generator import load_prefabs, generate_scene
from ligent.mlagents_envs.environment import UnityEnvironment
from ligent.utils import *
from flask import Flask, jsonify, request
import requests
from multiprocessing import Process
import subprocess
import socket
from colorama import Fore, Style
import time
import os
from typing import Dict

PORT_FOR_CLIENT = 9876
app = Flask(__name__)


@app.route("/")
def create_world():
    config = get_config()
    if "scenes_file" in config:
        response = load_json(config["scenes_file"][config["scenes_id"]])
        config["scenes_id"] = (config["scenes_id"] + 1) % len(config["scenes_file"])
    else:
        log(config["object_counts"])
        response = generate_scene(config["object_counts"])
    return jsonify(response)


@app.route("/config")
def create_config():
    config = get_config()
    log(f"request env config: {config}")
    response = {
        "id": config["id"],
        "time_scale": config["time_scale"],  # 20.0 is suitable for training
        "max_steps": config["max_steps"],  # 0 means infinite
        "buffer_file": config["buffer_file"],
    }
    return jsonify(response)


@app.route("/set_scenes")
def set_scenes():
    scenes = request.args.get("scenes")
    config = get_config()

    if scenes:
        config["scenes"] = scenes
        config["scenes_file"] = get_files_under(config["scenes"])
        config["scenes_id"] = 0
    else:
        if "scenes_file" in config:
            del config["scenes_file"]
    return jsonify({"status": "ok"})


@app.route("/set_object_counts")
def set_object_counts():
    object_counts = request.get_json().get("object_counts", {})
    config = get_config()
    config["object_counts"] = object_counts
    return jsonify({"status": "ok"})


# api provided for trainning code
def set_scenes_dir(scene_files_dir: str = "") -> bool:
    try:
        response = requests.get(
            f"http://localhost:{PORT_FOR_CLIENT}/set_scenes",
            params={"scenes": scene_files_dir},
        )
        return json.loads(response.text)["status"] == "ok"
    except Exception:
        return False
    

# api provided for trainning code
def set_object_counts(object_counts: Dict[str, int]) -> bool:
    try:
        response = requests.get(
            f"http://localhost:{PORT_FOR_CLIENT}/set_object_counts",
            headers={'Content-Type': 'application/json'},
            json={"object_counts": object_counts}
        )
        return json.loads(response.text)["status"] == "ok"
    except Exception:
        return False


def get_files_under(path):
    files = [
        file
        for file in os.listdir(path)
        if not os.path.isdir(os.path.join(path, file)) and str(file).endswith(".json")
    ]
    files = [os.path.join(config["scenes"], file) for file in sorted(files)]
    return files


DEFAULT_CONFIG = {
    "id": 0,
    "time_scale": 1.0,  # 20.0 is suitable for training
    "max_steps": 500,
    "scenes": "",
    "buffer_file": os.path.join(os.getcwd(), "game_states.json"),
    "object_counts": {}
}


def init_config():
    global config
    try:
        config = load_json("env_config.json")
        if config["scenes"]:
            config["scenes_file"] = get_files_under(config["scenes"])
            config["scenes_id"] = 0
    except Exception:
        config = DEFAULT_CONFIG
    return config


def get_config():
    try:
        return config
    except Exception:
        return init_config()


def serve():
    # Disable Flask logging
    import flask.cli

    flask.cli.show_server_banner = lambda *args: None
    #app.logger.disabled = True
    #logging.getLogger("werkzeug").disabled = True

    load_prefabs()
    log(Fore.GREEN + "LIGENT server started" + Style.RESET_ALL)
    app.run(debug=True, use_reloader=False, port=PORT_FOR_CLIENT, host="0.0.0.0")


def play_exec(executable_path, use_unity_env=False, skip_if_port_in_use=True):
    start_server_fork = False
    if skip_if_port_in_use:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            in_use = s.connect_ex(("localhost", PORT_FOR_CLIENT)) == 0
        if in_use:
            log("LIGENT server already started, skip")
        else:
            server = Process(target=serve)
            server.start()
            start_server_fork = True
    time.sleep(0.5)
    if use_unity_env:
        unity_env = UnityEnvironment(executable_path)
    else:
        process = subprocess.Popen(
            os.path.join(executable_path)
        )  # Launch the executable file

    try:
        while True:
            if use_unity_env:
                unity_env.step()
            else:
                pass
    except Exception as e:
        log("interrupted")
        if start_server_fork:
            server.terminate()
            server.join()
        if use_unity_env:
            unity_env.close()
        else:
            process.terminate()


def serve_fork(env_path):
    play_exec(env_path)
