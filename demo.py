import ligent

env = ligent.Environment(path="")
# you may change 'path' to the specific directory path containing the game executable file to avoid update checks on startup

try:
    # RL loop
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
        game_states = info["game_states"]

        # Example: if player grabs something, print the object
        # the game states may help you to calculate your custom reward
        if game_states["playerGrabInstance"] != -1:
            print(game_states["instances"][game_states["playerGrabInstance"]])

        # Example: if player say something, print the text
        if language_obs:
            print("Observation:", language_obs)

        # Example: store the first-person-view image of the playmate (AI agent)
        # !pip install scikit-image
        # import skimage
        # skimage.io.imsave("playmate_view.png", vision_observation)

        if done:
            observation, info = env.reset()
except Exception as e:
    print("Exception:", e)
finally:
    env.close()
