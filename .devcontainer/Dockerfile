FROM python:3.12-alpine

RUN apk update && apk add --no-cache \
    git \
    curl \
    zsh \
    bash \
    starship \
    openssh \
    pipx \
    make \
    gcc \
    python3-dev \
    musl-dev \
    linux-headers \
    && adduser -D -s /bin/zsh -u 1000 stilabs 

USER stilabs

ENV PATH="/home/stilabs/.local/bin:${PATH}"
ENV ZSH_THEME starship

COPY .zshrc /home/stilabs

SHELL ["/bin/zsh", "-c"]

RUN pipx install poetry --python $(which python) \
    && poetry config virtualenvs.create true \
    && poetry config virtualenvs.prefer-active-python true \
    && poetry config virtualenvs.in-project true


WORKDIR /workspace
COPY ../ .


CMD ["tail", "-f", "/dev/null"]