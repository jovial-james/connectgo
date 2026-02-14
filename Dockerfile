FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn mysql-connector-python bcrypt jinja2 python-multipart

EXPOSE 10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]