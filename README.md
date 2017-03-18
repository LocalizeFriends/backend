# backend
Application backend serving a REST API

## How to install
    virtualenv3 --always-copy venv && source venv/bin/activate && pip install -r requirements.txt && python localizefriends/manage.py migrate

## How to run development server
    source venv/bin/activate && python localizefriends/manage.py runserver

## HTTP statuses
* `200` – operation successful
* `400` – incorrect/insufficient parameters (see `message` and `errors` in returned)
* `403` – authentication error (see `message`; probably wrong/expired token)
* `500` – exception

## Supported API calls

### `POST /api/location`

Save current location of user behind `fbtoken`.

#### Parameters
* `fbtoken` – FB API access token
* `lng` – longitude in format `DDD.MMMMMM`
* `lat` – latitude in format `DD.MMMMMM`

#### Output
`message` and `error` are available only when `success` is `false`.

    {
       "success": true|false
       "message": "Message string.",
       "errors": { "field_name": ["Error message"] }
    }

### `GET /api/friends_locations`

Get latest locations (if available) of all friends of user behind `fbtoken`.

#### Parameters
* `fbtoken` – FB API access token

#### Output
    {
       "success": true,
       "data": [ { "name": "Contact Name", "id": "fb user id", location: null | {
            "timestamp_ms": milliseconds,
            "longitude": "DDD.MMMMMM",
            "latitude": "DD.MMMMMM"
            }}]
    }
