# backend
Application backend serving a REST API

## How to install
    virtualenv -p python3 --always-copy venv && source venv/bin/activate && ./instal_requirements.sh && python localizefriends/manage.py migrate

## How to run development server
    source venv/bin/activate && python localizefriends/manage.py runserver

**After each `git pull` one should apply new migrations which could have been made:**

    python localizefriends/manage.py migrate

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
* `lng` – longitude in format `(-)DDD.MMMMMMM`
* `lat` – latitude in format `(-)DD.MMMMMMM`

#### Output
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.

```
{
   "success": true|false,
   "message": "Message string.",
   "errors": { "field_name": ["Error message"] }
}
```

### `GET /api/friends_locations`

Get latest locations (if available) of all friends (who also use the app) of user behind `fbtoken`.

#### Parameters
* `fbtoken` – FB API access token

#### Output
* `data` is present when `success` is `true`.
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.

```
{
    "success": true|false,
    "data": [ { "name": "Contact Name", "id": fb user id, "location": null | {
        "timestamp_ms": milliseconds from epoch (UTC),
        "longitude": "DDD.MMMMMMM",
        "latitude": "DD.MMMMMMM"
        }}],
    "message": "Message string.",
    "errors": { "field_name": ["Error message"] }
}
```

### `GET /api/friends_within_range`

Get list of all friends (who also use the app) of user behind `fbtoken` who's distance from specified point is lower than `range`.

#### Parameters
* `fbtoken` – FB API access token
* `lng` – longitude of range center in format `(-)DDD.MMMMMMM`
* `lat` – latitude of range center in format `(-)DD.MMMMMMM`
* `range` – range radius in metres (integer)

#### Output
* `data` is present when `success` is `true`.
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.

```
{
    "success": true|false,
    "data": [ {
        "name": "Contact Name",
        "id": fb user id,
        "distance": metres from specified point
        "location": {
            "timestamp_ms": milliseconds from epoch (UTC),
            "longitude": "DDD.MMMMMMM",
            "latitude": "DD.MMMMMMM"
        }}],
    "message": "Message string.",
    "errors": { "field_name": ["Error message"] }
}
```

### `POST /api/meetup_proposal`

Create new meetup proposal with user behind `fbtoken` as organizer.

#### Parameters
* `fbtoken` – FB API access token
* `name` – name of the meetup
* `timestamp_ms` – UTC timestamp in milliseconds representing beginning of a meetup
* `place_name` – name of the meeting place
* `lng` – longitude in format `(-)DDD.MMMMMMM`
* `lat` – latitude in format `(-)DD.MMMMMMM`
* `invite` – comma separated list of Facebook user ids of friends to invite (who also use the app)

#### Output
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.

```
{
    "success": true|false,
    "message": "Message string.",
    "errors": { "field_name": ["Error message"] }
}
```

### `GET /api/meetup_proposals`

Get list of meetup proposals with user behind `fbtoken` as organizer or invitee.

#### Parameters
* `fbtoken` – FB API access token

#### Output
* `data` is present when `success` is `true`.
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.

```
{
    "success": true|false,
    "data": [
        {
            "id": meetup's id
            "organizer_id": fb user id,
            "creation_timestamp_ms": milliseconds from epoch (UTC),
            "name": "name of the meetup",
            "start_timestamp_ms": milliseconds from epoch (UTC),
            "place_name": "name of the meeting place",
            "longitude": "DDD.MMMMMMM",
            "latitude": "DD.MMMMMMM"
            "cancelled": true|false,
            "invitees": [
                {
                    "id": fb user id,
                    "accepted": true|false
                }
            ]
        }
    ]
    "message": "Message string.",
    "errors": { "field_name": ["Error message"] }
}
```


### `POST /api/meetup_proposal`

Create new meetup proposal with user behind `fbtoken` as organizer.

#### Parameters
* `fbtoken` – FB API access token
* `name` – name of the meetup
* `timestamp_ms` – UTC timestamp in milliseconds representing beginning of a meetup
* `place_name` – name of the meeting place
* `lng` – longitude in format `(-)DDD.MMMMMMM`
* `lat` – latitude in format `(-)DD.MMMMMMM`
* `invite` – comma separated list of Facebook user ids of friends to invite (who also use the app)

#### Output
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.

```
{
    "success": true|false,
    "message": "Message string.",
    "errors": { "field_name": ["Error message"] }
}
```


### `POST /api/meetup_proposal/{meetup_id}/accept`

Change acceptation flag for meetup with `meetup_id` to which user behind `fbtoken` was invited.

#### Parameters
* `fbtoken` – FB API access token
* `value` – 0 (invitation not accepted) or 1 (invitation accepted)

#### Output
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.

```
{
    "success": true|false,
    "message": "Message string.",
    "errors": { "field_name": ["Error message"] }
}
```


### `POST /api/meetup_proposal/{meetup_id}/cancel`

Change cancellation flag of the meetup organized by the user behind `fbtoken`.

#### Parameters
* `fbtoken` – FB API access token
* `value` – 0 (not cancelled) or 1 (cancelled)

#### Output
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.

```
{
    "success": true|false,
    "message": "Message string.",
    "errors": { "field_name": ["Error message"] }
}
```

### `POST /api/cloud_messaging_address`

Save new FCM address of the user app to send notifications to.

#### Parameters
* `fbtoken` – FB API access token of the app user
* `address` – FCM address
* `expiration_time_ms` – UTC timestamp in milliseconds representing the expiration time of the address

#### Output
* `message` is present when `success` is `false`.
* `errors` is present when there were some input validation errors.

```
{
    "success": true|false,
    "message": "Message string.",
    "errors": { "field_name": ["Error message"] }
}
```
