from typing import Tuple
from ligent.mlagents_envs.envs.unity_gym_env import UnityToGymWrapper
from ligent.mlagents_envs.environment import UnityEnvironment
from ligent.utils import *
import gym
import numpy as np
import struct
import logging


class Environment:
    def __init__(self, path: str = "") -> None:
        gym.logger.set_level(logging.CRITICAL)
        if not path:
            from huggingface_hub import snapshot_download
            path = snapshot_download(repo_id="chengzl18/ligent-windows", cache_dir='.game_client')
        unity_env = UnityEnvironment(path, no_graphics=False)
        self.env = UnityToGymWrapper(
            unity_env,
            uint8_visual=True,
            flatten_branched=False,
            allow_multiple_obs=True,
        )

    def reset(self):
        return self.env.reset()

    def step(
        self,
        move_right: int = 0,
        move_forward: int = 0,
        look_yaw: float = 0,
        look_pitch: float = 0,
        jump: bool = False,
        grab: bool = False,
        speak: str = "",
    ):
        while True:
            observation, reward, done, info = self.env.step(
                pack_action(
                    move_right, move_forward, look_yaw, look_pitch, jump, grab, speak
                )
            )
            vision_obs, language_obs = unpack_observation(observation)
            if language_obs != "[NOT_READY]":
                game_states = load_json('game_states.json')
                info['game_states'] = game_states
                return (vision_obs, language_obs), reward, done, info

    def close(self):
        self.env.close()


def pack_action(
    move_right: int = 0,
    move_forward: int = 0,
    look_yaw: float = 0,
    look_pitch: float = 0,
    jump: bool = False,
    grab: bool = False,
    speak: str = "",
):
    actions: np.ndarray = np.zeros(shape=(520), dtype=float)
    # 2 float for move(2 int), 2 float for look(2 float), 1 float for jump(1 bool), 1 float for grab(1 bool), 514 float remaining for chat
    TEXT_OFFSET = 6
    actions[0] = move_right
    actions[1] = move_forward
    actions[2] = look_yaw
    actions[3] = look_pitch
    actions[4] = jump
    actions[5] = grab

    b = speak.encode("utf-8")
    b = bytes([len(b)]) + b  # length indicator + content
    pad_len = len(actions) * 4 - len(b)
    b = b + b"\0" * pad_len  # content + padding
    # Pack the bytes into a float array
    float_array = struct.unpack("f" * (len(b) // 4), b)
    for i in range(0, len(actions) - TEXT_OFFSET):
        actions[TEXT_OFFSET + i] = float_array[i]
    return actions


def unpack_observation(observation) -> Tuple[np.ndarray, str]:
    vision: np.ndarray = observation[0]
    text: np.ndarray = observation[1]

    def parse_text(float_data):
        bytes_data = bytes(struct.pack("f" * len(float_data), *float_data))
        content_bytes_length = int(
            struct.unpack("B", bytes_data[:1])[0]
        )  # one byte for length, followed bytes for content
        content_bytes_data = bytes_data[1 : 1 + content_bytes_length]
        text = content_bytes_data.decode("utf-8")
        return text

    text = parse_text(text.data)
    return vision, text


def main():
    MAX_STEPS = 10000
    try:
        env = Environment()
        # env.reset()
        for i in range(10000):
            action = {
                "move_right": 0,
                "move_forward": 1,
                "look_yaw": 0.0,
                "look_pitch": 0.0,
                "jump": True,
                "grab": False,
                "speak": "",
            }
            observation, reward, done, info = env.step(**action)
            vision_obs, language_obs = observation
            if language_obs:
                log('language_obs',language_obs)
            if done or language_obs == "new" or (i + 1) % MAX_STEPS == 0:
                observation, info = env.reset()
    except Exception as e:
        log(e)
        env.close()
    env.close()


if __name__ == "__main__":
    main()
