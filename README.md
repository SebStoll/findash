# findash

A short description of the project.


## Running locally

To run a development instance locally, create a virtualenv, install the 
requirements from `requirements.txt` and launch `app.py` using the 
Python executable from the virtualenv.


## Docker 

In app.py: `app.run_server(host='0.0.0.0', port=8050, debug=True)`

In project root: `docker build -t findash .`

Check: `docker images`

Run: `docker run -p 8050:8050 findash`

Run: `docker run -v c:/workspace/findash/findash_data:/findash_data -p 8050:8050 findash`

If on windows: Dash is running on `http://127.0.0.1:8050/`

`docker ps`
`docker exec -it <container name> /bin/bash`




## Deploying on ECS

Use `make image` to create a Docker image. Then, follow [these 
instructions](https://www.chrisvoncsefalvay.com/2019/08/28/deploying-dash-on-amazon-ecs/) 
to deploy the image on ECS.