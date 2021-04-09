docker build --tag zpi-pwr .
docker run ^
	--rm ^
	--tty ^
	--interactive ^
	--volume //var/run/docker.sock:/var/run/docker.sock ^
	-p 5000:5000 ^
	-p 3306:3306 ^
	zpi-pwr:latest
