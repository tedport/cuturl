# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.14.3-alpine AS builder

WORKDIR /code
COPY requirements.txt /code
RUN pip3 install -r requirements.txt

COPY ./app ./app

COPY ./alembic ./alembic
COPY alembic.ini /code

COPY entrypoint.sh /code
RUN chmod +x /code/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/code/entrypoint.sh"]

FROM builder AS dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /

ENTRYPOINT ["/code/entrypoint.sh"]