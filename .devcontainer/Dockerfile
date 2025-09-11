FROM mcr.microsoft.com/vscode/devcontainers/base:alpine

ARG PYTHON_VERSION=3.13
ARG ALPINE_REPO=http://dl-cdn.alpinelinux.org/alpine/edge/community/

RUN apk update --no-cache --repository=${ALPINE_REPO} \
    && apk upgrade --no-cache --repository=${ALPINE_REPO} \
    && apk add --no-cache \
    bat fzf git go-task nodejs openjdk21 pnpm ripgrep sed uv \
    --repository=${ALPINE_REPO} \
    && rm -rf /var/cache/apk/* \
    # To make `task` command available
    && ln -s /usr/bin/go-task /usr/bin/task \
    # Install Python via uv
    && uv python install --preview --default ${PYTHON_VERSION}

USER vscode

WORKDIR /workspaces
