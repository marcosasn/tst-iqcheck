#!/usr/bin/env python
# coding: utf-8
#
# Set iqcheck as a custom command in config file.
# Eliane Araujo, 2016
# Marcos Nascimento, 2018

import sys
import tstlib

def add_command_iqcheck():
    config = tstlib.Config()
    if config.get('custom_commands') == None:
        config['custom_commands'] = {}
    if 'iqcheck' not in config.get('custom_commands').keys():
        config.get('custom_commands')['iqcheck'] = ['tst-iqcheck']
    
    config.save()
    
def main():
    add_command_iqcheck()
    print("iqcheck: tst iqcheck set") 
    return

if __name__ == "__main__":
    #just call main
    main ()