FROM python:3.10.20-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./app .
EXPOSE 8000
CMD ["python3", "-m", "uvicorn", "app.main:app", "--reload"]
