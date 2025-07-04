# Use official nginx image
FROM nginx:alpine

# Copy frontend files to nginx default public directory
COPY . /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start nginx server
CMD ["nginx", "-g", "daemon off;"]
