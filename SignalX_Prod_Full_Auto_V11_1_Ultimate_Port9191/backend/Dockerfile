FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
# Patched inline healthcheck (works on older Docker without heredoc support)
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=10   CMD python -c "import urllib.request,sys; import json; u=urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2); sys.exit(0 if u.getcode()==200 else 1)"
CMD ["python","main.py"]
