#!/usr/bin/env bash

gunicorn app:app --bind 0.0.0.0:8080 --log-level=debug --workers=4