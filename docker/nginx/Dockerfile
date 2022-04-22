FROM node:17.8.0-alpine as build

WORKDIR /build
COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./
RUN npm install
COPY ./frontend/ ./
RUN npm run build

FROM nginx:stable-alpine
RUN rm /etc/nginx/conf.d/default.conf

COPY --from=build /build/build /usr/share/nginx/html
COPY ./docker/nginx/run.sh ./run.sh
COPY ./docker/nginx/production/default.conf /etc/nginx/conf.d/
COPY ./docker/nginx/certbot/conf /etc/letsencrypt
COPY ./docker/nginx/certbot/www /var/www/certbot

RUN chmod +x /run.sh
CMD ["./run.sh"]