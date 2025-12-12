up_comics:
	docker-compose up --build

up_comics_clean:
	docker builder prune -f
	docker compose down -v
	docker compose up --build
