source venv/bin/activate
if [ -f "PID" ]; then
    kill $(cat PID)
    rm PID
fi
deactivate