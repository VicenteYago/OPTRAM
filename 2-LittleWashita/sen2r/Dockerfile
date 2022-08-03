################################### 
#       MULTI -STAGE BUILD        # 
###################################

FROM ranghetti/sen2r:latest 

RUN mkdir /home/sen2r
WORKDIR /home/sen2r

ADD ./*.json ./
ADD ./*.R    ./
COPY ./s2_tiles.rds /root/.sen2r/s2_tiles.rds

# INSTALL GCLOUD SUITE
RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-396.0.0-linux-x86_64.tar.gz -o /home/google-cloud-cli-396.0.0-linux-x86.tar.gz
RUN mkdir /home/google-cloud-sdk
RUN tar -xf /home/google-cloud-cli-396.0.0-linux-x86.tar.gz --directory /home
RUN /home/google-cloud-sdk/install.sh
