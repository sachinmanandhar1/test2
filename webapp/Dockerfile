FROM nginx:alpine

# Install Python and pip
RUN apk add --no-cache python3 py3-pip && \
    pip3 install requests --break-system-packages

# Create directory for HTML files
RUN mkdir -p /usr/share/nginx/html

# Copy HTML files
COPY index.html /usr/share/nginx/html/
COPY html/redirect.html /usr/share/nginx/html/

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy Python scripts
COPY publish_layers.py /
COPY publish_postgis_layers.py /

# Remove default configuration
RUN rm -f /etc/nginx/conf.d/default.conf