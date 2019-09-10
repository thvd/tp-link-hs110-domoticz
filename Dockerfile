FROM python:3-alpine
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY index.py /app/
CMD python ./index.py
