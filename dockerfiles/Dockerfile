FROM ubuntu/apache2

RUN echo 'ServerName 127.0.0.1' >> /etc/apache2/apache2.conf && echo 'Hi there, what is love?' > /var/www/html/index.html

CMD /usr/sbin/apache2ctl -D FOREGROUND

EXPOSE 80
