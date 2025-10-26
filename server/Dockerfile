FROM ghcr.io/astral-sh/uv:latest

WORKDIR /server/

COPY ./python-version ./
RUN uv python install

COPY pyproject.toml ./
RUN uv run sync --upgrade --no-dev

COPY ./src/ ./src/
ENV PYTHONPATH=./src/

CMD ["uv", "run", "--no-dev", "litestar", "--app", "src.main:app", "run"]
