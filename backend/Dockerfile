FROM ghcr.io/astral-sh/uv:python3.13-alpine

RUN apk update && apk add --no-cache gcc libc-dev

WORKDIR /backend



# Copy dependencies first (for caching layers)
COPY pyproject.toml .
RUN uv pip compile pyproject.toml -o requirements.txt
RUN uv pip install -r requirements.txt --system

# Copy project AFTER installing deps
COPY . .

