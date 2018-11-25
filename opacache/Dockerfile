FROM redis

ADD pyauthz.py /
ADD config.ini /data/
ADD run.sh /
RUN apt-get update
RUN apt-get -y install python3 python3-pip
RUN pip3 install requests && \
    pip3 install Flask && \
    pip3 install redis
CMD /run.sh
#CMD ["python3", "/pyauthz.py"]

