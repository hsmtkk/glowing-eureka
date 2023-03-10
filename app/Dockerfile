FROM python:3.11 AS runtime

WORKDIR /app

# Cloud Profiler needs build environment
RUN apt-get -y update \
 && apt-get install -y build-essential

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY app.py /app/app.py

ENTRYPOINT ["python"]
CMD ["/app/app.py"]
