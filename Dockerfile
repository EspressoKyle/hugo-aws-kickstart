FROM python:3.11.4-buster
ADD main.py .
ADD .env .
RUN pip install boto3
CMD ["python", "./main.py"]