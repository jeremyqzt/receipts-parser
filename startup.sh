#!/usr/bin/env bash
service nginx start
uwsgi --ini wsgi.ini
