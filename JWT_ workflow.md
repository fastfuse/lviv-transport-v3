# JWT Authorization workflow

### Endpoints:

* /auth/register
* /auth/login
* /auth/logout



### Registration

Request:

    POST: /auth/register
    HEADERS: content-type: application/json
    BODY: {"username":"user1", "password":"user1"}

Response:
```json
    {
        "auth_token": "<auth_token>",
        "message": "Successfully registered.",
        "status": "Success"
    }
```

### Login

Request:

    POST: /auth/login
    HEADERS: content-type: application/json
    BODY: {"username":"user1", "password":"user1"}

Response:

```json
    {
        "auth_token": "<auth_token>",
        "message": "Successfully logged in.",
        "status": "Success"
    }
```

### Logout

Request:
```
    POST: /auth/logout
    HEADERS: content-type: application/json, Authorization: "Bearer <auth_token>"
```

Response:

```json
    {
        "message": "Successfully logged out.",
        "status": "Success"
    }
```
