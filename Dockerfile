FROM python:3.12


RUN pip install python-dotenv discord.py paho-mqtt
ADD .env .
ADD src/* ./
CMD ["python", "./main.py"]