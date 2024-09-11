FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app


EXPOSE 5000

ENV FLASK_ENV=development

RUN export PYTHONPATH="${PYTHONPATH}:/app/app"

CMD ["python", "main.py"]
#CMD ["ls", "/app/"]
