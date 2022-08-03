### 1 - Compile & Run container
```{bash}
sudo docker-compose build 
sudo docker-compose up -d 
```

### 2 - Get into the container

```{bash}
sudo docker ps
```
```{bash}
./toDocker <container-id>
```

### 3 - Configure GCLOUD 

```{bash}
cd /home/google-cloud-sdk/bin
./gcloud init
```

And log in with your google account

### 4 - Configure sen2r
```{r}
R -e "sen2r::check_gcloud(gsutil_dir='/home/google-cloud-sdk/')"
```

### 5 - Run script 

```{bash}
cd /home/sen2r
./runSentinel.sh ./inputs-config.json ./littleWashita.json 'LittleWashita' '2019-01-01' '2020-01-01'
```
