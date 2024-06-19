FROM python:3.9.2-alpine

RUN apk update

RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app
COPY . ./

RUN pipenv install --system --deploy

EXPOSE 5000
ENTRYPOINT ["/usr/src/app/run-dev.sh"]