#!/usr/bin/env python3

"""
Main upload script for c211

Given the path to the handins (submissions), uploads all of the information. 
"""

import uploader
import re
import os
import ConfigParser
import sys

roster_re = re.compile(r'^.*\.roster$')
THE_CONFIG = '../config.cfg'
USAGE= "upload.py <assignment>"

def main(): 
    if len(sys.argv) != 2:
        print(USAGE)
        return

    config = ConfigParser.ConfigParser()
    config.read(THE_CONFIG)
    handins_path = config.get('paths', 'handins')
    sections = config.get('config', 'sections')
    
    assignment = sys.argv[1]
    all_sections = os.path.join(handins_path, assignment)
    if(sections):
        for section in os.listdir(all_sections):
            traverse_section(assignment, all_sections, section)
    else:
        traverse_section(assignment, all_sections, "Unknown")

def traverse_section(assignment, all_sections, section):
    for handin in os.listdir(os.path.join(all_sections, section)):
        filename = os.path.join(all_sections, section, handin)
        username = handin.split('.')[0]
        uploader.upload_submission(username, assignment, filename, section)
        
if __name__ == "__main__": main()
