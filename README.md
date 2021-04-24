# recipes

## Setting up
1. Create an empty `.env` file.
2. Copy a `docker-compose.override.yml`
```
cp .devops/docker/docker-compose.override.yml.example docker-compose.override.yml
```
3. Fill in `!!UID!!` with your uid (`echo $UID`)
4. Build images
```
docker-compose build
```
5. Run the project
```
docker-compose up -d
```
