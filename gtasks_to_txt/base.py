import json
import os
from loguru import logger as log


def load_export(export_path="Takeout"):
    with open(file=f"{export_path}/Tasks/tasks.json") as f:
        tasks = load_lists(f)
    return tasks


def load_lists(f):
    tasks_json = json.loads(f.read())
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
        item["list"] = list_title
    return items


def convert_gtasks_to_notes(gtasks):
    notes = []
    child_notes = []
    for task in gtasks:
        note = convert_gtask_to_notes(task)
        if note["parent"]:
            child_notes.append(note)
        else:
            notes.append(note)
    log.debug(json.dumps([child_notes[0], notes[0]], indent=4))
    notes = set_child_notes(notes, child_notes)
    return notes


def convert_gtask_to_notes(task):
    note = {
        "id": task["id"],
        "title": task["title"],
        "updated": task["updated"],
        "list": task["list"],
    }
    note["isCompleted"] = True if task["status"] == "completed" else False
    note["parent"] = task["parent"] if "parent" in task else None
    note["details"] = task["notes"] if "notes" in task else None
    note["due"] = task["due"] if "due" in task else None
    note["created"] = task["created"] if "created" in task else None
    note["completed"] = task["completed"] if "completed" in task else None
    return note


def set_child_notes(notes, child_notes):
    updated_notes = []
    parent_ids = [n["parent"] for n in child_notes]
    updated_notes.extend([n for n in notes if n["id"] not in parent_ids])
    parent_notes = [n for n in notes if n["id"] in parent_ids]
    updated_parent_notes = []
    # for child in child_notes:
    #     parent_note = [n for n in parent_notes if n["id"] == child["parent"]][
    #         0
    #     ]
    #     if "children" not in parent_note:
    #         parent_note["children"] = []
    #     parent_note["children"].append(child)
    #     updated_parent_notes.append(parent_note)
    
    return updated_notes
