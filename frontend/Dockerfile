# Use lightweight nginx image
FROM nginx:alpine

# Remove default nginx website files
RUN rm -rf /usr/share/nginx/html/*

# Copy your custom index.html into nginx web root
COPY index.html /usr/share/nginx/html/index.html

# Replace default nginx config with your custom config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

