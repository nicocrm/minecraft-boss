# Welcome to the MineBoss repository!

## Objectives

- Build a website to manage the running minecraft servers.

## Project organization

The project consists of 2 applications:

- a Python API, in the [api](api) folder,
- a Vue UI, in the [vue-ui](vue-ui) folder

## Development environment requirements

For the Python API:

- python >= 3.6
- pipenv

For the VueJS UI:

- node >= 14
- npm

## Getting started

This will install dependencies for both API and UI applications, and run them concurrently for
development:

    npm install
    npm start

By default the UI will run on port 8080 and the API on port 8000.  The development server includes a
proxy for API request such that the UI can make HTTP request on `/api` without having the use CORS.

## Production operation

- Build the production version of the vue-js application

      cd vue-ui && npm build

- Alternatively, you can use a docker container to do the build:

      cd vue-ui && ./build.sh

- Create a service for the API
- Set up a reverse proxy to serve the application files (from vue-ui/dist) and proxy requests to
  /api to the API service.

## Unit tests

Run unit tests in the root folder with:

    npm test
