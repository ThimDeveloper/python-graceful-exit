FROM --platform=linux/amd64 python:3.10.8@sha256:3352d050e90bc0fccd8cbd8993b988ebbb2bb402558934d48d94ea9bcca418b7 as base


ENV PROJECTDIR package
WORKDIR ${PROJECTDIR}
RUN pip install --no-cache-dir graceful-exit
COPY src .
COPY bin/entrypoint.sh /usr/local/bin/entrypoint.sh 

ENV PYTHONPATH=$PYTHONPATH:$PROJECT_DIR

CMD [ "/usr/local/bin/entrypoint.sh" ]