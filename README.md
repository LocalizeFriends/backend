# backend
Application backend serving a REST API

## How to install
    virtualenv3 --always-copy venv && source venv/bin/activate && pip install -r requirements.txt && python localizefriends/manage.py migrate

## How to run development server
    source venv/bin/activate && python localizefriends/manage.py runserver

## HTTP statuses
* `200` – operation successful
* `400` – incorrect/insufficient parameters (see `message` and `errors` in returned)
* `403` – authentication error or was action forbidden (see `message`; probably wrong/expired token)
* `500` – exception

## Supported API calls

### `POST /api/location`

Save current location of user behind `fbtoken`.

#### Parameters
* `fbtoken` – FB API access token
* `lng` – longitude in format `(-)DDD.MMMMMM`
* `lat` – latitude in format `(-)DD.MMMMMM`

#### Output
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.


    {
       "success": true|false,
       "message": "Message string.",
       "errors": { "field_name": ["Error message"] }
    }

### `GET /api/friends_locations`

Get latest locations (if available) of all friends (who also use the app) of user behind `fbtoken`.

#### Parameters
* `fbtoken` – FB API access token

#### Output
* `data` is present when `success` is `true`.
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.


    {
        "success": true|false,
        "data": [ { "name": "Contact Name", "id": "fb user id", location: null | {
            "timestamp_ms": milliseconds from epoch (UTC),
            "longitude": "DDD.MMMMMM",
            "latitude": "DD.MMMMMM"
            }}],
        "message": "Message string.",
        "errors": { "field_name": ["Error message"] }
    }


### `POST /api/meetup_proposal`

Create new meetup proposal with user behind `fbtoken` as organizer.

#### Parameters
* `fbtoken` – FB API access token
* `name` – name of the meetup
* `timestamp_ms` – UTC timestamp in milliseconds representing beginning of a meetup
* `place_name` – name of the meeting place
* `lng` – longitude in format `(-)DDD.MMMMMM`
* `lat` – latitude in format `(-)DD.MMMMMM`
* `invite` – comma separated list of Facebook user ids of friends to invite (who also use the app)

#### Output
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.


    {
       "success": true|false,
       "message": "Message string.",
       "errors": { "field_name": ["Error message"] }
    }
