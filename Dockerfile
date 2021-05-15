FROM python:3.9-buster
COPY . /ate

WORKDIR /ate
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]