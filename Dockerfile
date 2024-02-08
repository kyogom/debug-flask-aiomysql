FROM python:3.11.2-alpine
RUN apk update && \
    apk add --no-cache build-base libffi-dev openssl-dev zlib-dev libffi-dev libc-dev gcc python3-dev && \
    apk del openssl-dev
ADD requirements.txt /tmp/
RUN pip3 install cffi
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /app
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=5001"]
