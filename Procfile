web: gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT
release: flask --app app db upgrade || true
