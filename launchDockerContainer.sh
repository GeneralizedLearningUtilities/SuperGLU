docker run --name superglu -p 80:80 superglu &
sleep 1s
docker exec superglu sudo service nginx start