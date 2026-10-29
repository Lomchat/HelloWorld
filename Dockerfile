# syntax=docker/dockerfile:1.7
# =============================================================================
# hello-world - Production container image
# =============================================================================
# Multi-stage build:
#   1. builder: builds the wheel in an isolated environment.
#   2. runtime: installs the wheel in a minimal image, running as non-root.

ARG PYTHON_VERSION=3.12

# -----------------------------------------------------------------------------
# Stage 1: build the wheel
# -----------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR /build

# Install the build frontend first to leverage the layer cache.
RUN pip install --no-cache-dir build==1.2.2

# Copy only what is needed to build the package.
COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN python -m build --wheel --outdir /dist

# -----------------------------------------------------------------------------
# Stage 2: minimal runtime image
# -----------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime

LABEL org.opencontainers.image.title="hello-world" \
      org.opencontainers.image.description="A robust, production-ready Hello World application." \
      org.opencontainers.image.source="https://github.com/Lomchat/HelloWorld" \
      org.opencontainers.image.licenses="MIT"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Run as an unprivileged user.
RUN groupadd --system --gid 10001 hello \
    && useradd --system --uid 10001 --gid hello --no-create-home --shell /usr/sbin/nologin hello

COPY --from=builder /dist/*.whl /tmp/

RUN pip install /tmp/*.whl && rm -f /tmp/*.whl

USER hello:hello

# Verify that the application produces the canonical greeting.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["sh", "-c", "hello-world | grep -qxF 'Hello, World!'"]

ENTRYPOINT ["hello-world"]
