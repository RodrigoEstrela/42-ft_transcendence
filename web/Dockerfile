FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/web

COPY requirements.txt /app/web/

# Build psycopg2-binary from source -- add required required dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/web/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
