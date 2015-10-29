FROM ubuntu:14.04


# Install dependencies
RUN bash ./setup.sh
RUN bash ./local.sh

EXPOSE 80

CMD ["/usr/sbin/apache2", "-D",  "FOREGROUND"]
