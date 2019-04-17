build:
	docker build -t player:1.4 .

run:
	docker run -d --rm -p 5000:5000 -v ~/Projekty/Acc/tvnplayer-prod/v1.4/data/:/home/player/data/:rw --name p1 player:1.4

export:
	docker image save player:1.4 > player-latest.tar

clean:
	find . -type d -name __pycache__ -exec rm -r {} \; || true
	find . -type d -name .ropeproject -exec rm -r {} \; || true
	find player/static/cache -type f -delete || true
	find player/data -type f -iname \*.json -delete || true
	find player/data -type f -iname \*.jpg -delete || true

