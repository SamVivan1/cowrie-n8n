FROM python:3.11-slim
WORKDIR /app
COPY forwarder.py .
RUN pip install requests
CMD ["python", "forwarder.py"]
