#!/usr/bin/env python
endpoints = {
    "createusers": {
        "endpoint":"/api/users",
        "action":"POST",
        "description":"Create user"
    },
    "getusersdetails": {
        "endpoint":"/api/users/{id}",
        "action":"GET",
        "description":" Get user details"
    },
    "createtranscations": {
        "endpoint":"/api/transactions",
        "action":"POST",
        "description":"Create user"
    },
    "gettransactions": {
        "endpoint":"/api/transactions/{userId}",
        "action":"GET",
        "description":" Get user details"
    }
}

