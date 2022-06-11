# topoclust
Is a server / client application used to explore the results of a significance mode clustering algorithms pipeline.
You can find the available resources in the resource folder. If you want to add a different data set, just place it there and
start the software, it will detect the new file.

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