# This is used to build bindings for arm64
FROM python:3.10.6-slim-bullseye

RUN apt update && apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev libbz2-dev g++ make

WORKDIR .
COPY . .

RUN cd blst && sed -i 's/cflags="-D__ADX__ $cflags"/echo "adx skip"/' build.sh && ./build.sh
