# topoclust
Is a server / client application used to explore the results of a significance mode clustering algorithms pipeline.
This application is designed to help astronomers find potential clusters within large amounts of data by offering a visualization of the solution space produced by the significance mode clustering.

Below you will find simple instructions to work with this application.

# Install

Install all the dependencies by executing the command below

```shell
./install.sh
```

# Development mode

Start the development mode by executing

```shell
./start.sh
```

This will execute both, the backend python flask server and the fronted Vue.js UI.

# Production mode

Execute 

```shell
docker-compose up
```

To build docker containers for the backend and frontend and run it in production mode.


# Add new resources
Supported resource file types:
- comma-separated values, text/csv (.csv)

## Development mode
If you are working with the development mode and you would like to add a resource for clustering, you can simply place that file into
```shell
lodestar-backend/resources/import
```
