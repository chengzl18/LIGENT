from ligent.server.scene_generator import load_prefabs, generate_scene
from ligent.mlagents_envs.environment import UnityEnvironment
from ligent.utils import *
from flask import Flask, jsonify
from multiprocessing import Process
import subprocess
import socket
from colorama import Fore, Style
import time
import os

PORT_FOR_CLIENT = 9876
app = Flask(__name__)


@app.route("/")
def create_world():
    config = get_config()
    if "scenes_file" in config:
        response = load_json(
            os.path.join(config["scenes"], config["scenes_file"][config["scenes_id"]])
        )
        config["scenes_id"] = (config["scenes_id"] + 1) % len(config["scenes_file"])
    else:
        response = generate_scene()
    return jsonify(response)


@app.route("/config")
def create_config():
    config = init_config()
    response = {
        "id": config["id"],
        "time_scale": config["time_scale"],  # 20.0 is suitable for training
        "max_steps": config["max_steps"],  # 0 means infinite
        "buffer_file": config["buffer_file"],
    }
    return jsonify(response)


def get_files_under(path):
    files = [
        file
        for file in os.listdir(path)
        if not os.path.isdir(os.path.join(path, file)) and str(file).endswith(".json")
    ]
    return files


DEFAULT_CONFIG = {
    "id": 0,
    "time_scale": 1.0,  # 20.0 is suitable for training
    "max_steps": 500,
    "scenes": "",
    "buffer_file": os.path.join(os.getcwd(), "game_states.json"),
}

def init_config():
    global config
    try:
        config = load_json("env_config.json")
        if config["scenes"]:
            config["scenes_file"] = get_files_under(config["scenes"])
            config["scenes_id"] = 0
        log('request env config:',config)
    except Exception:
        config = DEFAULT_CONFIG
    return config


def get_config():
    try:
        print(config)
        return config
    except Exception:
        return DEFAULT_CONFIG


def serve():
    # Disable Flask logging
    import flask.cli

    flask.cli.show_server_banner = lambda *args: None
    app.logger.disabled = True
    logging.getLogger("werkzeug").disabled = True

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
        process = subprocess.Popen(os.path.join(executable_path))  # Launch the executable file

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
