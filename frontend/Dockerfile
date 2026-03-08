# Build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .

# Accept the API URL at build time
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
