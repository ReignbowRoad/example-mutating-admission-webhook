FROM ubuntu:latest

RUN apt-get update \
   && apt-get install -y \
      python3 \
      python3-pip \
   && rm -rf /var/lib/apt/lists/*

RUN mkdir /app

COPY requirements.txt /app/requirements.txt
ADD src /app

RUN pip3 install \
   --break-system-packages \
   --requirement /app/requirements.txt

EXPOSE 8443

ENTRYPOINT [ "python3", "/app/main.py" ]
