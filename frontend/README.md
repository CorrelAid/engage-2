# Engage Frontend

This is the frontend for the CorrelAid Engage project. It is a Vue.js app using Vite as a bundler. It uses vue-router for routing and vuetify for the UI components.

## Dev env setup

To setup the dev environment you need to have node.js and a package manager
installed. For the following instructions we assume that you have npm installed.

1. Go to the frontend folder

1. Install dependencies

        npm install

1. Install pre-commit hooks via the backend folder. See the backend README for
   details.

## Local deployment

To run the frontend locally you can use the following command:

    npm run dev

This will start a local server on port 3000. You can then access the frontend
at http://localhost:3000.

### Backend

The frontend expects the backend to be available at http://localhost:8000. To
start the backend locally see the backend README for details. Alternatively you
can use the docker-compose setup to start the backend. For this you need to

1. Go to the root folder of the project

1. Start the backend

        docker-compose up

## Selected npm scripts

This section only aims to provide a short overview of the most important
npm scripts. For a full list of commands see the `package.json`.

- `npm run dev`: Starts the development server
- `npm run generate-client`: TBD
