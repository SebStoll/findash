# https://towardsdatascience.com/how-to-use-docker-to-deploy-a-dashboard-app-on-aws-8df5fb322708
# https://flaviocopes.com/docker-access-files-outside-container/
# https://www.digitalocean.com/community/tutorials/how-to-share-data-between-the-docker-container-and-the-host

FROM continuumio/miniconda3

COPY requirements.txt /tmp/
COPY ./app /app
WORKDIR "/app"

RUN conda install --file /tmp/requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]