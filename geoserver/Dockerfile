FROM kartoza/geoserver:latest

ENV CATALINA_OPTS="-server -Xms1024m -Xmx2048m -Dgeoserver.login.autocomplete=on"
ENV GEOSERVER_DATA_DIR=/opt/geoserver_data
ENV SKIP_DEMO_DATA=true
ENV ROOT_WEBAPP_REDIRECT=false
ENV CORS_ENABLED=true
ENV INSTALL_EXTENSIONS=false