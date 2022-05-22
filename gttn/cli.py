import json
from loguru import logger as log
from .base import load_export, convert_gtasks_to_notes, write_lists_to_disk, convert_notes_to_lists

def main():
    
    # get folder location from sys args
    gtasks = load_export()
    notes = convert_gtasks_to_notes(gtasks)
    lists = convert_notes_to_lists(notes)
    # log.debug(sum([ len(lists[l]) for l in lists ]))
    file_paths = write_lists_to_disk(lists)
    # log.debug(sum([ len(f) for f in file_paths ]))
    # log.debug(json.dumps(file_paths, indent=2))