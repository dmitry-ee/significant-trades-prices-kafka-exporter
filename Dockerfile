FROM        python:3.7-alpine
ARG         APP_DIR=/app/
ARG         SRC_DIR=src
ARG         USER_NAME=stpke

WORKDIR     ${APP_DIR}

COPY        ${SRC_DIR}/requirements_base.txt    ${APP_DIR}
COPY        docker-entrypoint.sh                ${APP_DIR}

RUN         set -ex ;\
            apk add bash gcc musl-dev ;\
            pip install -r requirements_base.txt ;\
            chmod +x docker-entrypoint.sh ;\
            rm -rf /var/lib/apt/lists/* ;\
            rm -rf /var/cache/apk/*

COPY        ${SRC_DIR}                          ${APP_DIR}/${SRC_DIR}

ENV         PATH=.:$PATH

ENTRYPOINT  ["docker-entrypoint.sh"]

CMD ["run"]
