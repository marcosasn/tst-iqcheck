#!/usr/bin/env python
# coding: utf-8
#
# Set qcheck as a custom command in config file.
# Eliane Araujo 2016

import sys
import tstlib

def add_command_qcheck():
    config = tstlib.Config()
    if config.get('custom_commands') == None:
        config['custom_commands'] = {}
    if 'qcheck' not in config.get('custom_commands').keys():
        config.get('custom_commands')['qcheck'] = ['tst-qcheck']
    
    config.save()
    
def main():
    add_command_qcheck()
    return

if __name__ == "__main__":
    #just call main
    main ()