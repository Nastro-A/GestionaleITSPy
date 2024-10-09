#!/bin/sh
# Copyright (C) 2024 Nastro_
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
set -e 

echo "Build: $BUILD"

if [ "$BUILD" = "false" ]; then 
    echo "Eseguo le migrazioni e avvio il server..."

    python manage.py makemigrations
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    echo "Avvio Gunicorn..."
    gunicorn GestionaleITS.wsgi:application --bind 0.0.0.0:$PORT

elif [ "$BUILD" = "true" ]; then
    echo "Eseguo le migrazioni, creo l'utente admin e avvio il server..."

    python manage.py makemigrations
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput

    python manage.py createsuperuser --noinput

    echo "Avvio Gunicorn..."
    gunicorn GestionaleITS.wsgi:application --bind 0.0.0.0:$PORT

else
    echo "Errore: la variabile 'build' deve essere 'true' o 'false'. Valore attuale: $BUILD"
    exit 1
fi
