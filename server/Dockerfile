FROM alpine:latest AS oqs

WORKDIR /oqs/

RUN apk update
RUN apk upgrade
RUN apk add --no-cache build-base
RUN apk add --no-cache git
RUN apk add --no-cache cmake
RUN apk add --no-cache openssl-dev
RUN git clone -b 0.12.0 --depth 1 https://github.com/open-quantum-safe/liboqs.git ./
RUN cmake -S ./ -B ./build/ -DCMAKE_INSTALL_PREFIX=./install/ -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE=Release
RUN cmake --build ./build/ --target install --config Release -j $(nproc)


FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /server/

RUN apk update
RUN apk upgrade
RUN apk add --no-cache git

ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

COPY ./.python-version ./
RUN uv python install

COPY pyproject.toml ./
RUN uv sync --upgrade --no-dev

COPY ./src/ ./src/
ENV PYTHONPATH=./src/
COPY --from=oqs /oqs/install/ ./libs/oqs/

CMD ["/bin/sh", "-c", "uv run --no-dev litestar --app src.main:app run -H 0.0.0.0 -p $SERVER_PORT -W $(nproc)"]
