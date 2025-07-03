# Use official Nginx image
FROM nginx:alpine

# Optional: custom Nginx config
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static files into Nginx's public directory
COPY . /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
