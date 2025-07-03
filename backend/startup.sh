#!/bin/bash
echo "Iniciando la aplicación con Gunicorn..."
gunicorn --bind 0.0.0.0:8000 --timeout 600 --workers 4 back:app