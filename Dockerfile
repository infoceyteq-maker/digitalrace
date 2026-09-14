# Ceyteq website + backend — one container, no external services.
#   docker build -t ceyteq .
#   docker run -p 8000:8000 -v ceyteq-data:/data \
#         -e CEYTEQ_ADMIN_PASSWORD='YourStrongPassword' ceyteq
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CEYTEQ_DATA_DIR=/data \
    PORT=8000

WORKDIR /app
COPY . /app

# the database, the session secret and uploaded images live on the volume
VOLUME ["/data"]
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python3 -c "import urllib.request,os;urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','8000')+'/api/health',timeout=4)" || exit 1

CMD ["python3", "server.py", "--host", "0.0.0.0"]
