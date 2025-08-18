FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY best.pt .
COPY templates/ templates/
COPY static/ static/

EXPOSE $PORT

CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app"]
