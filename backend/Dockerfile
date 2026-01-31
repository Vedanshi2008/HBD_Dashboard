FROM python:3.11-slim

WORKDIR /app

# 1. Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# 2. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. Install Browser (Only re-runs if requirements.txt changes)
RUN playwright install --with-deps chromium

# 4. Create temp directory
RUN mkdir -p /app/tmp/uploads

# 5. Copy the rest of the code (This is the only step that repeats frequently)
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "gunicorn app:app -b 0.0.0.0:${PORT:-8000}"]