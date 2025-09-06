FROM mcr.microsoft.com/vscode/devcontainers/base:alpine

RUN apk add --no-cache \
    bat ripgrep sed \
    && rm -rf /var/cache/apk/*

USER vscode

WORKDIR /workspaces
