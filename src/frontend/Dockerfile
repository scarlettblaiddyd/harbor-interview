FROM oven/bun:latest

WORKDIR /app

COPY package.json bun.lock ./
RUN bun install

COPY . .

EXPOSE 5173
CMD ["bun", "run", "dev", "--host", "0.0.0.0"]

# RUN bun run build

# # Serve with a static server
# FROM nginx:alpine
# WORKDIR /app
# RUN npm install -g serve
# COPY --from=build /app/dist /usr/share/nginx/html

# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]