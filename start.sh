docker build --build-arg ENVIRONMENT=PRODUCTION -t engage-api ./backend
docker build -t engage-client ./frontend
docker network create engage-network || echo "Creating engage-network docker network failed."
docker run -d --rm --env-file .env.dev --network engage-network --network-alias api --name engage-api --publish 8000:8000 engage-api:latest sh -c 'gunicorn api.app:app --workers=2 --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --access-logfile -' || echo "Starting engange-api failed."
docker run -d --rm --network engage-network --network-alias client --name engage-client --publish 8080:80 engage-client:latest || echo "Starting engange-client failed."
