#!/bin/bash

cd /home/otranto/projects/marioai/downloads
#python loader2.py /home/otranto/projects/marioai/downloads/archives/ /home/otranto/projects/marioai/out/production/Marioai /home/otranto/projects/marioai/log.txt /home/otranto/projects/marioai/out/production/Marioai/ yes

python ./load.py -ufrom /home/otranto/projects/marioai/downloads/archives/ -uto /home/otranto/projects/marioai/out/production/Marioai -log /home/otranto/projects/marioai/log.txt -benchmark /home/otranto/projects/marioai/out/production/Marioai/ -delete no
