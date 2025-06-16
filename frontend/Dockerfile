FROM node:22.13.1-alpine

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY . .
RUN npm run build

RUN apk add --no-cache nginx \
  && mkdir -p /var/www/html \
  && cp -r dist/* /var/www/html/ \
  && rm -rf node_modules src public

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
