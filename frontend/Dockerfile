FROM node:lts-alpine

COPY package*.json ./

RUN npm install

# make the 'app' folder the current working directory
WORKDIR /app


# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .
