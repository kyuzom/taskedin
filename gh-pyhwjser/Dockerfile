FROM python:3.10.0

LABEL Author="KyuzoM"
LABEL E-mail="kyuzom@googlegroups.com"
LABEL version="0.0.4"

ENV PYTHONDONTWRITEBYTECODE 1

# custom port
ENV HWSERIAL_PORT 5001
EXPOSE 5001

COPY . /pyhwjser
RUN pip install --upgrade pip
RUN pip install -r /pyhwjser/requirements.txt
CMD python /pyhwjser/pyhwjser/pyhwjser.py
