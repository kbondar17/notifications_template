#!/bin/sh

exec python email_worker.py &
exec python dead_letters_worker.py