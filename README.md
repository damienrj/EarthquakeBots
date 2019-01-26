# EarthquakeBots
To build image
```
docker build -t earthquake .
```

To run interactively
```
docker run -v ~/Development/EarthquakeBots/data:/app/data -it earthquake bash
```

Push newest version to dockerhub
```
docker tag earthquake damienrj/earthquakebots:0.0.0
docker push damienrj/earthquakebots:0.0.0
```




