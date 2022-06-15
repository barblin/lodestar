# topoclust
Is a server / client application used to explore the results of a significance mode clustering algorithms pipeline.

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
If you would like to add a resource to work with during development, you can simply place that file into
```shell
lodestar-backend/resources/import
```
