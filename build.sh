#!/usr/bin/env bash
pip install -r requirements.txt
py manage.py collectstatic --noinput
py manage.py migrate