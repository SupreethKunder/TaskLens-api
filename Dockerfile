FROM python:3.13.0-slim-bullseye

RUN useradd --create-home --uid 999 --shell /bin/bash devops \
    && mkdir -p /home/devops \
    && chown -R 999:999 /home/devops \
    && chmod -R u+w /home/devops

WORKDIR /home/devops

ENV VIRTUALENV=/home/devops/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --chown=devops dist/*.whl /tmp/

RUN pip install -U pip \
    && pip install --no-cache-dir -U /tmp/*.whl \
    && rm -rf /tmp/*.whl

EXPOSE 5000

