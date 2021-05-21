POST $server/host/

Sent
```
{
   registration_key: "key",
   mac_address: "00:00:00:00:00:00"
}
```
Response
```
{
   guid: "GUID"
}
```

POST $server/host/is_valid

Sent
```
{
   guid: "GUID"
}
```

Response
```
{
   is_valid: true/false
}
```