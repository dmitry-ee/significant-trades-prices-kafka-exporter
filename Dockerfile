FROM        python:3.7-alpine
ARG         APP_DIR=/app/
ARG         SRC_DIR=src
ARG         USER_NAME=stpke

WORKDIR     ${APP_DIR}

COPY        ${SRC_DIR}                          ${APP_DIR}/${SRC_DIR}
COPY        docker-entrypoint.sh                ${APP_DIR}
COPY        ${SRC_DIR}/requirements_base.txt    ${APP_DIR}

RUN         set -ex ;\
            apk add --no-cache bash ;\
            pip install -r requirements_base.txt ;\
            chmod +x docker-entrypoint.sh ;\
            rm -rf /var/lib/apt/lists/* ;\
            rm -rf /var/cache/apk/*

ENV         PATH=.:$PATH

ENTRYPOINT  ["docker-entrypoint.sh"]

CMD ["run"]
