FROM nginx:latest

# Copy custom nginx config
COPY fvb.conf /etc/nginx/conf.d/fvb.conf

# Create directory for certificates
RUN mkdir -p /etc/nginx/certs

# Generate self-signed certificate
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/certs/selfsigned.key \
  -out /etc/nginx/certs/selfsigned.crt \
  -subj "/C=IN/ST=fvb/L=fvb/O=fvb/OU=fvb/CN=fvb"

# Expose port 8443 and 9443 for SSL
EXPOSE 8443
EXPOSE 9443