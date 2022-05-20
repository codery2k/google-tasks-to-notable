import json
from pathlib import Path
from loguru import logger as log
from . import config
from slugify import slugify


def load_export(export_path=config.EXPORT_PATH):
    with open(file=f"{export_path}/{config.EXPORT_FILE_PATH}") as f:
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
    updated_notes.extend(
        [n for n in non_child_notes if n["id"] not in unique_parent_ids]
    )
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


def write_notes_to_disk(notes):
    output_path = ensure_dir(config.OUTPUT_PATH)
    # log.error(type(output_path))
    # log.debug(output_path)
    file_paths = []
    for note in notes:
        file_path = create_note_file(note, output_path)
        if file_path:
            file_paths.append(file_path)
    return file_paths


def ensure_dir(path):
    dir = Path(path)
    if not dir.exists():
        dir.mkdir(parents=True, exist_ok=True)
    return dir


def create_note_file(note, output_path):
    file_path = None
    note_title = note["title"]
    if note_title and ("."!=note_title):
        sanitized_title = slugify(note_title, max_length=30)
        file_name = f"{output_path}/{sanitized_title}.txt"
        with open(file_name, "w") as f:
            f.write(json.dumps(note, indent=2))
        # https://stackoverflow.com/questions/11348953/how-can-i-set-the-last-modified-time-of-a-file-from-python
    return file_path


