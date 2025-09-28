FROM nginx:alpine
RUN apk add --no-cache python3 py3-pip && pip3 install requests --break-system-packages
COPY index.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY publish_layers.py /
COPY publish_postgis_layers.py /