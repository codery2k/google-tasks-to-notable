import json
from loguru import logger as log
from .base import load_export, convert_gtasks_to_notes, write_notes_to_disk

def main():
    
    # get folder location from sys args
    gtasks = load_export()
    notes = convert_gtasks_to_notes(gtasks)
    log.error(len(notes))
    file_paths = write_notes_to_disk(notes)
    log.debug(file_paths)