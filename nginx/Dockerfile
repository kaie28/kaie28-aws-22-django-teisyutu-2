FROM nginxinc/nginx-unprivileged:1.25-alpine
USER root
RUN apk update && apk upgrade --no-cache
RUN mkdir -p /var/log/nginx /var/cache/nginx /usr/src/app/static /usr/src/app/media && chown -R nginx:nginx /var/log/nginx /var/cache/nginx /usr/src/app
RUN rm -f /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d/default.conf
RUN chown nginx:nginx /etc/nginx/conf.d/default.conf
RUN sed -i 's|/var/run/nginx.pid|/tmp/nginx.pid|g' /etc/nginx/nginx.conf
USER nginx
VOLUME ["/usr/src/app/static", "/usr/src/app/media"]
CMD ["nginx", "-g", "daemon off;"]
