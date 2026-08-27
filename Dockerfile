# AltayebAmer.com — local test image (pure static site, no build step)
FROM nginx:alpine

# Serve the site
COPY . /usr/share/nginx/html
# Custom config: clean URLs + correct MIME + no-cache during testing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
