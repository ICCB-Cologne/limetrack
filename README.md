# Sample_tracking
Prototype for sampling tracking tasks

## Prerequisites
Docker

## Setup

### Clean Volume On Reboot

`docker compose -f docker-compose.yml -f docker-compose-develop.yml up --remove-orphans --force-recreate`

### Persist Volumes On Reboot

`docker compose -f docker-compose.yml -f docker-compose-develop.yml up --remove-orphans`

