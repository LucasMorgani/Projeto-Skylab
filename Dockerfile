FROM python:3.11-alpine

WORKDIR /app

# Dependências de build
RUN apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Usuário não-root
RUN adduser -D skylab && chown -R skylab:skylab /app
USER skylab

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]