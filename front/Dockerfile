FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

FROM nginx:1.25-alpine

COPY --from=builder /app/dist /var/www/html

EXPOSE 8080

CMD ["nginx -g 'daemon off;'"]