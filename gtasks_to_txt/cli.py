import json
from logging import error, info
# from gtasks_to_txt.base import load_export, convert_gtasks_to_notes
from .base import load_export

def main():
    
    # get folder location from sys args
    gtasks = load_export()
    # info(json.dumps(gtasks, indent=4))
    # notes = convert_gtasks_to_notes(gtasks)
    # error(json.dumps(notes, indent=4))
    
