FROM node:alpine

RUN npm install -g http-server

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build
RUN chmod +x ./execute.sh

CMD [ "./execute.sh" ]