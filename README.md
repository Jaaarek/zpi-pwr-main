# Linki i opis

Program służy do zarządzania dostępem, na podstawie rozpoznawania twarzy

Link do strony:
http://zpipwr2021.atthost24.pl/login

hasło i login:
admin / admin

Hosting:
https://secure.atthost.pl/login/
hasło i login
zpipwr2021 / zpipwr2021

1. Zainstaluj Dockera i przejdz przez tutorial, musisz takze zainstalowac linuxa za pomocą poradników:
https://www.docker.com/
https://docs.microsoft.com/pl-pl/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package

2. Aby odpalić aplikacje, odpal terminal w lokalizacji projektu i wpisz "run.bat"
3. Aby zakończyć działanie naciśnij CLTR+C

# Docker


Docker-compose.yml jest to plik w którym znajdują się wszystkie usługi które się odpalają za jednym razem.
Konwencja tworzenia jest bardzo prosta, najlepiej tworzyc nazwy, tak jak nazywaja sie foldery.
Porty ustalamy w docker-compose i dockerfile aplikacji.

uruchamiamy appke run.bat



## build
docker build --tag zpi-pwr .

## run

### MacOS

docker run \
	--rm \
	--volume /var/run/docker.sock:/var/run/docker.sock \
	-p 5000:5000 \
	-p 3306:3306 \
	zpi-pwr:latest

### Windows

docker run ^
	--rm ^
	--volume //var/run/docker.sock:/var/run/docker.sock ^
	-p 5000:5000 ^
	-p 3306:3306 ^
	zpi-pwr:latest

## exec

### MacOS

docker run \
	--rm \
	--interactive \
	--tty \
	--volume /var/run/docker.sock:/var/run/docker.sock \
	-p 5000:5000 \
	-p 3306:3306 \
	--entrypoint /bin/bash \
	zpi-pwr:latest

### Windows

docker run ^
	--rm ^
	--interactive ^
	--tty ^
	--volume //var/run/docker.sock:/var/run/docker.sock ^
	-p 5000:5000 ^
	-p 3306:3306 ^
	--entrypoint /bin/bash ^
	zpi-pwr:latest