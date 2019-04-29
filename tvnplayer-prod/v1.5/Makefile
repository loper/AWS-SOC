build:
	docker build -t hesp.pl:3333/player:1.5 .

run:
	docker run -d --rm -p 5000:5000 -v ~/Projekty/Acc/tvnplayer-prod/v1.5/data/:/home/player/data/:rw --name p1 hesp.pl:3333/player:1.5

export:
	# docker image save hesp.pl:3333/player:1.5 > player-latest.tar
	docker push hesp.pl:3333/player:1.5

clean:
	find . -type d -name __pycache__ -exec rm -r {} \; || true
	find . -type d -name .ropeproject -exec rm -r {} \; || true
	find player/static/cache -type f -delete || true
	find player/data -type f -iname \*.json -delete || true
	find player/data -type f -iname \*.jpg -delete || true

