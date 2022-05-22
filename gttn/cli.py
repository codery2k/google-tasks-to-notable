import json
from loguru import logger as log
from .base import load_export, convert_gtasks_to_notes, write_notes_to_disk

def main():
    
    # get folder location from sys args
    gtasks = load_export()
    notes = convert_gtasks_to_notes(gtasks)
    file_paths = write_notes_to_disk(notes)
    # log.debug(sum([ len(f) for f in file_paths ]))
    # log.debug(json.dumps(file_paths, indent=2))