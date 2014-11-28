ENVIRONMENT = development
PROJECT_NAME = imghost
PYTHON_COMMAND = python2.7

#################################
#################################
#################################

ARGS_INLINE = -e ENVIRONMENT=$(ENVIRONMENT) PROJECT_NAME=$(PROJECT_NAME) PYTHON_COMMAND=$(PYTHON_COMMAND)
CFLAGS = -c -g -D $(ENVIRONMENT) -D $(PROJECT_NAME) -D $(PYTHON_COMMAND)

#################################

default:
	$(MAKE) run $(ARGS_INLINE)

install:
	$(MAKE) virtualenv $(ARGS_INLINE)
	$(MAKE) deploy $(ARGS_INLINE)
	$(MAKE) flush $(ARGS_INLINE)
	$(MAKE) loaddata $(ARGS_INLINE)
	$(MAKE) search $(ARGS_INLINE)
	$(MAKE) createcachetable $(ARGS_INLINE)
	
deploy:
	$(MAKE) upgrade $(ARGS_INLINE)
	$(MAKE) syncdb $(ARGS_INLINE)
	#$(MAKE) cron $(ARGS_INLINE)
	$(MAKE) collectstatic $(ARGS_INLINE)
	
virtualenv:
	virtualenv ../../virtualenv/$(PROJECT_NAME)

#################################

cron:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py installtasks --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT); \
	)

upgrade:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		pip install -r requirements/common.txt; \
		pip install -r requirements/$(ENVIRONMENT).txt; \
	)
	
flush:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py flush --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT) --noinput; \
	)

run:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py runserver localhost:8000 --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT); \
	)

clean:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py sqlclear main --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT) | $(PYTHON_COMMAND) manage.py dbshell --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT); \
	)
	-rm -rf build
	-rm -rf *~*
	-find . -name '*.pyc' -exec rm {} \;

test:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py test --noinput --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT); \
	)

syncdb:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py syncdb --noinput --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT); \
	)
	
dumpdata:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
	 	$(PYTHON_COMMAND) manage.py dumpdata --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT) > main/fixtures/$(ENVIRONMENT).json; \
	)

dumpall:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
	 	$(PYTHON_COMMAND) manage.py dumpdata --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT) > main/fixtures/all.json; \
	)
 
loaddata:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py loaddata $(ENVIRONMENT).json --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT); \
		$(PYTHON_COMMAND) manage.py loaddata all.json --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT); \
	)

collectstatic:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py collectstatic --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT) --noinput; \
	)
	
search:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py build_solr_schema --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT) > /usr/share/solr/conf/schema.xml; \
		service tomcat6 restart; \
		$(PYTHON_COMMAND) manage.py rebuild_index --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT) --noinput; \
	)

update_index:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py update_index --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT); \
	)

createcachetable:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py createcachetable cache --verbosity 0 --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT); \
	)

createflat:
	( \
		. ../../virtualenv/$(PROJECT_NAME)/bin/activate; \
		$(PYTHON_COMMAND) manage.py createflat --settings=$(PROJECT_NAME).settings.$(ENVIRONMENT); \
	)
