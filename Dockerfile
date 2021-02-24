FROM ubuntu:20.04
# Base configurations
RUN apt -y update && \
    apt -y install \
    git \
    python3.8 \
    python3-pip
# Project configurations
EXPOSE 8000
ENV SECRET_KEY="?x>V:h&w0O#7P*4/&fEFe[WsM6>G4b>_orH}^#mcmC])bV,oR}"
WORKDIR /workspace
RUN git clone https://github.com/johannesssf/physical-legal-goods-api.git && \
    cd physical-legal-goods-api && \
    pip3 install -r requirements.txt && \
    python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    python3 manage.py shell -c "from django.contrib.auth import get_user_model; \
        get_user_model().objects.create_superuser('admin', 'admin@email.com', '123456')"
# Starts the container with application up
ENTRYPOINT [\
    "python3",\
    "/workspace/physical-legal-goods-api/manage.py",\
    "runserver",\
    "0.0.0.0:8000"]
