#!/bin/bash

cd /home/mickael/Projets/UpTimeDelay
source env/bin/activate
python manage.py cron massive_run
