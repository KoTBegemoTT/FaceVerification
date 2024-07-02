FROM debian:bookworm

ENV TERM xterm

# Настройки темы https://github.com/romkatv/powerlevel10k
COPY .p10k.zsh /root/
COPY .zshrc /root/

# Нужно для работы deepface. Автоматически подтверждает установку.
RUN apt-get update && yes | apt-get install libgl1
RUN apt-get update && yes | apt-get install libglib2.0-0
