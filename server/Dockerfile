FROM ghcr.io/astral-sh/uv:latest

WORKDIR /server/

COPY ./python-version ./
RUN uv run python install

COPY pyproject.toml ./
RUN uv run sync --upgrade --no-dev

COPY ./src/ ./

CMD ["uv", "run", "--no-dev", "litestar", "--app", "main:app", "run"]
