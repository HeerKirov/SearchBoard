source venv/bin/activate
nohup gunicorn app:app -b 0.0.0.0:8000 --reload >> SERVER.LOG 2>&1 &
echo $! > PID
echo web server started.
deactivate