# Dependences

- python 3
- pip

`pip install -r requirements.txt`

# Example of .env needs to be mounted in docker compose file

```
DEBUG= (True or False)
DJANGO_SUPERUSER_USERNAME= (username of superuser)
DJANGO_SUPERUSER_PASSWORD= (password of superuser)
DJANGO_SUPERUSER_EMAIL= (email of superuser)
SECRET_KEY= (django secret key at least 30 characters and 5 simbols and numbers)
SERVER_ADDRESS= (url of hosting for the app)
DB_NAME= (name of db)
DB_USER= (username of db)
DB_PASS= (password of db)
DB_HOST= (ip/url of db host)
DB_PORT= (db port)
MEDIA_ROOT= (path for medias)
GOOGLE_CLIENT_ID= (Google Client ID from the google cloud console)
GOOGLE_SECRET= (Google Secret from google cloud console)
GOOGLE_KEY= (generally empty)
```

# Docker Compose example

```yaml
 services:
  gestionale:
        image: nastroa/gestionaleits:release
        restart: always
        volumes:
          - path/to/media/folder:/gestionale/media
          - path/to/env/file:/gestionale/.env
        environment:
          - PORT=8000
          - BUILD=false #if true creates the superuser, if already done please set it false
        expose:
          - "8000" #must match with env port
        networks:
          - nginx
        depends_on:
          - db
          - nginx
  db:
    image: postgres
    restart: always
    volumes:
      - path/to/postgres/data:/var/lib/postgresql/data/pgdata
    environment:
      POSTGRES_DB: #db name
      POSTGRES_PASSWORD: #db password
      PGDATA: /var/lib/postgresql/data/pgdata
    expose:
      - "5432"
    networks:
      - nginx
  nginx:
        image: nginx:stable
        restart: unless-stopped
        ports:
          - "80:80"
          - "443:443"
        volumes:
          - path/to/nginx/conf:/etc/nginx/nginx.conf
          - path/to/certificate/generated/with/certbot:/etc/nginx/cert.crt
          - path/to/key/generated/with/certbot:/etc/nginx/cert.key
        networks:
        - nginx
networks:
  nginx:
    external: true
```

# TODO

- Default value of association "Pagamento effettuato"
- import of storage, computers, courses.
- Tables Sorting with filters

# Licence

This project is under the MPL 2.0

If you want to contribute insert in every file this header:
> This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
