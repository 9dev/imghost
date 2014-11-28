# imghost

Imghost is a Django project created for educational purposes.


## Installation

```
$ apt-get install libjpeg-dev libxml2-dev libxslt1-dev python-dev solr-tomcat redis-server
$ make install
```

Additionally, to enable search engine:

* Prepare search schema:

```
$ sudo make search
```

* Edit the following files and change the port to 8983

```
/etc/solr/conf/scripts.conf
/etc/tomcat6/server.xml
```

* Restart Tomcat:

```
$ sudo service tomcat6 restart
```

To run installed project with default settings:

```
$ make
```

## Final notes

* Tested on Ubuntu Desktop 14.04 LTS.
* This project is closed. There are no planned updates in the future.

