# build stage
FROM node:18-alpine AS build-stage
WORKDIR /vue_app
COPY package.json ./
RUN npm install --omit=dev
COPY . .
RUN npm run build

# production stage
FROM nginx AS production-stage
COPY --from=build-stage /vue_app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
