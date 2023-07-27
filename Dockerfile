# Dockerfile
FROM python:3.11
WORKDIR /webtronics_TZ
COPY . /webtronics_TZ
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
