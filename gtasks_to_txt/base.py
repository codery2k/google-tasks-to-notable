import json
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
    non_child_notes = []
    child_notes = []
    for task in gtasks:
        note = convert_gtask_to_notes(task)
        if note["parent"]:
            child_notes.append(note)
        else:
            non_child_notes.append(note)
    notes = set_child_notes(non_child_notes, child_notes)
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


def set_child_notes(non_child_notes, child_notes):
    updated_notes = []
    updated_parent_notes = []
    parent_ids = [n["parent"] for n in child_notes]
    unique_parent_ids = list(set(parent_ids))  
    updated_notes.extend([n for n in non_child_notes if n["id"] not in unique_parent_ids])
    parent_notes = [n for n in non_child_notes if n["id"] in unique_parent_ids]
    for child in child_notes:
        existing_parent_note_array = [
            n for n in updated_parent_notes if n["id"] == child["parent"]
        ]
        if existing_parent_note_array:
            existing_parent_note = existing_parent_note_array[0]
            existing_parent_note["children"].append(child)
        else:
            parent_note = [n for n in parent_notes if n["id"] == child["parent"]][0]
            parent_note["children"] = []
            parent_note["children"].append(child)
            updated_parent_notes.append(parent_note)
    updated_notes.extend(updated_parent_notes)
    return updated_notes
