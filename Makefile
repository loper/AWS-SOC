run:
	docker run -it -d --name soc -v data:/data/ -p 5000:5000 soc:1.0
build:
	docker build -t soc:1.0 .
clean:
	find . -type d -name __pycache__ -exec rm -r {} \; || true
	find . -type d -name .ropeproject -exec rm -r {} \; || true
	docker rm -f soc || true

