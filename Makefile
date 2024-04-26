#!/usr/bin/make
SHELL=/bin/bash


build:
	@docker-compose --progress plain build --parallel

up:
	@docker-compose up

upd:
	@docker-compose up -d

start:
	@docker-compose start

stop:
	@docker-compose stop

clear:
	@docker-compose down

logs-tail:
	@docker-compose logs -f --tail="20"

