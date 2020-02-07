FROM python:3.8-slim-buster

ENV UNIT_VERSION 1.14.0

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
            build-essential curl wget && rm -rf /var/lib/apt/lists/* \
    && cd /tmp && wget -qO - "http://unit.nginx.org/download/unit-$UNIT_VERSION.tar.gz" | tar xvz \
    && cd unit-$UNIT_VERSION \
    && ./configure --prefix=/usr \
                 --modules=lib --control='unix:/var/run/control.unit.sock' \
                 --log=/dev/stdout \
                 --pid=/var/run/unitd.pid \
    && ./configure python --config=/usr/local/bin/python-config \
    && make install \
    && rm -rf /tmp/unit-$UNIT_VERSION \
    && apt-get remove --auto-remove -y build-essential wget

WORKDIR /home/f5demo
COPY requirements.txt /config/requirements.txt
RUN pip install --no-cache-dir -r /config/requirements.txt
COPY . .

STOPSIGNAL SIGTERM

RUN unitd \
    && curl -X PUT --data-binary @config/config.json --unix-socket /var/run/control.unit.sock http://localhost/config \
    && ln -sf /dev/stdout /var/log/unit.log
CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]