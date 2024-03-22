# Borrar estas líneas si no existen imágenes
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -aq)
# ---
docker build -t server -f Dockerfile_server .
docker run -d -p 12345:12345 server
docker build -t client -f Dockerfile_client .
winpty docker run -it --env HOST_IP=host.docker.internal --env PORT=12345 client
