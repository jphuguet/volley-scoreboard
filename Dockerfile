FROM python:alpine3.18

RUN adduser --system --no-create-home scoreboard

WORKDIR app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
RUN chown -R 100:100 /app/data

USER scoreboard
EXPOSE 3000

CMD ["python", "main.py"]
