FROM node:latest

WORKDIR /xeokitApp

COPY package*.json ./

RUN npm install

COPY . .

CMD [ "npm", "run", "serve"]