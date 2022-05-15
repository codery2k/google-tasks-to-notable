
import json
import os
from loguru import logger as log


def load_export(export_path="Takeout"):
    with open(file= f"{export_path}/Tasks/tasks.json") as f:
        tasks = load_lists(f)
    log.info(json.dumps(len(tasks), indent=4))
    return tasks

def load_lists(f):
    tasks_json=json.loads(f.read())
    lists = tasks_json["items"]
    tasks = []
    for list in lists:
        items = loads_tasks(list)
        tasks.extend(items)
    return tasks

def loads_tasks(list):
    list_title = list["title"]
    items = list["items"]
    for item in items:
        # log.info(item.keys())
        item["list"] = list_title
    return items

