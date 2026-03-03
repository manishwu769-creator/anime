FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY blitex_anime_bot.py .
CMD ["python3", "blitex_anime_bot.py"]
