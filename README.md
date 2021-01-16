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

Run: `docker run -v c:/workspace/findash/findash_data:/findash_data -p 8050:8050 findash`

If on windows: Dash is running on `http://127.0.0.1:8050/`

Bash into container: `docker ps` for container name, then `docker exec -it <container name> /bin/bash`


## Deploying on EC2

https://towardsdatascience.com/deploying-a-python-web-app-on-aws-57ed772b2319

`ssh -i "dash_webserver.pem" ubuntu@ec2-3-127-149-234.eu-central-1.compute.amazonaws.com`

`git clone https://github.com/SebStoll/findash.git`

Docker (Ubuntu image):

`sudo apt-get update`

`sudo apt install docker.io`

`sudo systemctl start docker`

`sudo systemctl enable docker`

`docker --version`

In project root: `sudo docker build -t findash .`

Run: `docker run -v /home/ubuntu/findash/findash_data:/findash_data -p 80:8050 findash`

http://3.127.149.234/

To access the web app, use the instance’s Public DNS IPv4 which can 
be found on the EC2 running instance dashboard (eg `3.127.149.234`). 
Copy and paste the address into your browser, and you’ll see the application.




## Deploying on ECS

Use `make image` to create a Docker image. Then, follow [these 
instructions](https://www.chrisvoncsefalvay.com/2019/08/28/deploying-dash-on-amazon-ecs/) 
to deploy the image on ECS.