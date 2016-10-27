#!/bin/bash
wget https://bootstrap.pypa.io/get-pip.py
export PATH=$PATH:/home/PORTOALEGRE/$(whoami)/.local/bin
python get-pip.py --user
pip2.7 install scipy --user
