FROM python:3.8
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=on \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=10 \
  PYSETUP_PATH="/opt/pysetup" \
  LC_ALL=C.UTF-8 \
  LANG=C.UTF-8

WORKDIR /app

# Install requirements
COPY Makefile requirements.txt requirements.dev.txt /app/
RUN make install

# Copy source
COPY development /app/development

# Copy config and tests files
COPY .editorconfig flake8.tests.ini MANIFEST.in setup.py setup.cfg /app/
COPY tests /app/tests
