try {
    & "$env:DOCMAKER_HOME\.venv\Scripts\activate.ps1"
    python "$env:DOCMAKER_HOME\main.py" $args
}
finally {
    deactivate
}