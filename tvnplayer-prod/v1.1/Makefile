build:
	docker build -t player:latest .

run:
	docker run -d --rm -p 5000:5000 -v ~/Projekty/Acc/tvnplayer-prod/v1.0/data/:/home/player/data/:ro --name p1 player

clear:
	@find . -type d -name __pycache__ -exec rm -r {} \;
	find player/static/cache -type f -delete
	find player/data -type f -iname \*.json -delete

