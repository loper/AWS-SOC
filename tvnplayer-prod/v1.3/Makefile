build:
	docker build -t player:1.3 .

run:
	docker run -d --rm -p 5000:5000 -v ~/Projekty/Acc/tvnplayer-prod/v1.3/data/:/home/player/data/:rw --name p1 player:1.3

export:
	docker image save player:1.3 > player-latest.tar

clean:
	find . -type d -name __pycache__ -exec rm -r {} \;
	find . -type d -name .ropeproject -exec rm -r {} \;
	find player/static/cache -type f -delete
	find player/data -type f -iname \*.json -delete
	find player/data -type f -iname \*.jpg -delete

