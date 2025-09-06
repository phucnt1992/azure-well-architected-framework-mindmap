FROM mcr.microsoft.com/vscode/devcontainers/base:alpine

RUN apk update  \
    && apk add --no-cache \
    bat fzf git go-task nodejs npm openjdk21 python3 ripgrep sed \
    && rm -rf /var/cache/apk/* \
    # To make `task` command available
    && ln -s /usr/bin/go-task /usr/bin/task

USER vscode

WORKDIR /workspaces
