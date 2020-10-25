FROM node:13.12.0-alpine

WORKDIR /usr/src/app

ENV PATH /usr/src/app/node_modules/.bin:$PATH
ENV REACT_APP_EXCHANGE_OPERATIONS_SERVICE_URL=http://localhost:5000

COPY package.json /usr/src/app/package.json
COPY package-lock.json /usr/src/app/package-lock.json
RUN npm install
RUN npm ci
RUN npm install react-scripts@3.4.1 -g --silent

COPY . ./

CMD ["npm", "start"]
