# The first stage
# Build React static files
FROM node:13.12.0-alpine as build

WORKDIR /app/frontend
COPY ./../frontend/package.json ./
COPY ./../frontend/package-lock.json ./
RUN npm ci --silent
COPY ./../frontend/ ./
RUN npm run build


FROM nginxinc/nginx-unprivileged:1-alpine
LABEL MAINTAINER="ShayestehHS"

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000


COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY --from=build /app/frontend/build /usr/share/nginx/html
COPY ./run.sh /run.sh

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/defult.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]