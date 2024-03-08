FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-dev 

RUN apt-get install -y python3-pip
RUN pip install flask
RUN pip install flask-login

RUN apt-get install -y git
RUN git clone https://github.com/Menaerus/Imatgik.git

ENV FLASK_APP=.
EXPOSE 5000

WORKDIR Imatgik

CMD ["flask", "run", "--host", "0.0.0.0"]