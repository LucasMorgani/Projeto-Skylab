FROM python:3.13.2-alpine3.20

EXPOSE 5000

WORKDIR /skylab_app

COPY app.py .
COPY ./templates ./templates
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
