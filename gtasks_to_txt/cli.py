import json
from loguru import logger as log
from .base import load_export, convert_gtasks_to_notes

def main():
    
    # get folder location from sys args
    gtasks = load_export()
    notes = convert_gtasks_to_notes(gtasks)
    log.error(json.dumps(notes[0], indent=4))