import logging
import json


def log(*args):
    logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger("LIGENT")
    logger.error(*args)


def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def store_json(obj, file):
    with open(file, "w", encoding="utf-8") as f:
        return json.dump(obj, f, ensure_ascii=False, indent=4)
