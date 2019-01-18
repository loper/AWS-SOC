build:
	docker build -t player:latest .

run:
	docker run -d --rm -p 5000:5000 -v ~/Projekty/Acc/tvnplayer-prod/v1.1/data/:/home/player/data/:rw --name p1 player

export:
	docker image save player:latest > player-latest.tar

clear:
	@find . -type d -name __pycache__ -exec rm -r {} \;
	find player/static/cache -type f -delete
	find player/data -type f -iname \*.json -delete

