docker build --tag zpi-pwr .
docker run ^
	--rm ^
	--name kutas ^
	--tty ^
	--interactive ^
	--volume //var/run/docker.sock:/var/run/docker.sock ^
	-p 10000:10000 ^
	zpi-pwr:latest
