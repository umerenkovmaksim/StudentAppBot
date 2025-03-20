FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 6000

CMD ["python", "src/bot.py"]