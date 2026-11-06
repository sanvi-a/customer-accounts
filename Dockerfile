FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY accounts/ ./accounts/
COPY wsgi.py .

# Run as a non-root user
RUN useradd --uid 1000 theia && chown -R theia /app
USER theia

ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --log-level=info wsgi:app"]
