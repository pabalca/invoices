FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive
ENV FLASK_ENV=production
ENV FLASK_APP=/usr/src/app/invoices
ENV FLASK_ENCRYPTION_KEY=changethispleasenow

RUN apt update && apt-get install -y python3-pip
RUN mkdir -p /usr/src/app/invoices
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD invoices /usr/src/app/invoices
RUN flask initdb
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000","invoices:app"]
