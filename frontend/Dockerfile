# Build react code
FROM node:22-alpine as builder
WORKDIR /usr/src
COPY react-search-bar-main .
RUN npm ci
RUN npm run build

# Create webserver
FROM nginx:mainline

# Copy configuration
COPY nginx.conf /etc/nginx/nginx.conf

# see https://www.rockyourcode.com/run-docker-nginx-as-non-root-user/
RUN chown -R nginx:nginx /usr/share/nginx/html && chmod -R 755 /usr/share/nginx/html && \
        chown -R nginx:nginx /var/cache/nginx && \
        chown -R nginx:nginx /var/log/nginx && \
        chown -R nginx:nginx /etc/nginx/conf.d
RUN touch /var/run/nginx.pid && \
        chown -R nginx:nginx /var/run/nginx.pid

# Copy code ready for distribution
COPY --from=builder /usr/src/dist /usr/share/nginx/html

USER nginx
