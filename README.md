# Kisseklyv

## Create kisse

`POST /kisse`

**Reponse**

- `201 Created` on success
```json
{
  "identifier": "af23ce8"
}
```


## Delete kisse

**Response**

- `204 No Content` on success
- `404 Not Found` if the kisse does not exist

## Get info for kisse

**Definition**

`GET /kisse/<kisse_id>`

**Response**

- `200 OK` on success
- `404 Not Found` if the kisse does not exist

```json
{
  "identifier": "af23ce8",
  "people": ["Adam", "Bertil", "Cesar"],
  "expenses": [
    {"Adam": 10},
    {"Adam": 200},
    {"Bertil": 50}
  ]
}
```
