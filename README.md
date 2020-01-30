# Kisse

## Create kisse

`POST /kisse`

**Arguments**
- description: a description of the kisse

**Reponse**

- `201 Created` on success
```json
{
  "message": "Kisse created",
  "data": {
      "kisse_id": "af23ce8"
  }
}
```


## Delete kisse

`DELETE /kisse`

**Arguments**

* kisse_id (required)

**Response**

- `204 No Content` on success
- `404 Not Found` if the kisse does not exist

## Modify kisse

`PUT /kisse`

## Get info for kisse

**Definition**

`GET /kisse`

**Arguments**

* kisse_id (required)

**Response**

- `200 OK` on success
- `404 Not Found` if the kisse does not exist

```json
{
  "kisse_id": "af23ce8",
  "people": ["Adam", "Bertil", "Cesar"],
  "description": "Ski trip",
  "expenses": [
    {"Name":  "Adam", "Amount":  10, "Description":  "Food"},
    {"Name":  "Adam", "Amount":  50, "Description":  "Drink"},
    {"Name":  "Bertil", "Amount":  100, "Description":  "Misc"}
  ]
}
```

# Person

## Create a new person
`POST /person`

**Arguments**
- kisse_id
- name

**Response**
- `409 Conflict` if the person name is not unique within the kisse
- `201 Created` on success
```json
{
  "message": "Person created",
  "data": {
      "person_id": "ab23ce8"
  }
}
```

## Get info about person
`GET /person`

**Arguments**

- kisse_id
- person_id

**Response**

- `200 OK` on success
- `404 Not Found` if the person does not exist

```json
{
  "person_id": "cb67a",
  "name": "Kalle"
}
```
