FROM ubuntu:14.04
MAINTAINER saymagic saymagic@163.com
RUN apt-get update
RUN apt-get install -y nginx
COPY ./www /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
