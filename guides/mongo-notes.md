# Some notes about the mongodb

If you ever need to backup and free the mongodb you can run this command to create a backup from the data.

```bash
mongodump --gzip ./mongodump-2020-10-20
```

And then this one to clean all collections in the `opendatacam` db
```bash
mongo opendatacam --eval "db.getCollectionNames().forEach(function(n){db[n].remove()});"
```
