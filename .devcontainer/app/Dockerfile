FROM debian:bookworm

ENV TERM xterm

# Настройки темы https://github.com/romkatv/powerlevel10k
COPY .p10k.zsh /root/
COPY .zshrc /root/

# Нужно для работы deepface. Автоматически подтверждает установку.
RUN apt-get update -yqq && apt-get install -yqq libgl1-mesa-glx
