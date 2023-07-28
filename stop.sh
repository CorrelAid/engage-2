docker stop engage-api || echo "Stopping engage-api failed."
docker stop engage-client || echo "Stopping engage-client failed."
docker network rm engage-network || echo "Removing engage-network docker network failed."
