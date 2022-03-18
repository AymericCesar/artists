FROM python:3

# install Python 3
RUN pip install --upgrade pip
RUN pip install flask flask_httpauth

CMD ["python", "/var/www/html/server.py"]
