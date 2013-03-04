# TODO:

* remove masshealth/data/auth.json 

## Solved:

#128, Issue #129

git filter-branch --index-filter 'git rm --cached --ignore-unmatch auth.json' \
  --prune-empty --tag-name-filter cat -- --all

* add maps to data stories
* deploy

DATA MAPS

# Notes

masshealth layer ids:
[5, 12, 13, 22, 27, 37, 38, 39, 40, 29, 47, 57, 59, 60, 61, 65, 66, 68, 56, 1, 14, 52, 20, 69]



layers failed:
fair_market_median_rent_2013_zip*

/usr/local/var/tomcat

/Users/cspanring/Projects/geonode/geoserver_data


from django.core.mail import send_mail
send_mail('Test email', 'test body', 'webapp@mapc.org', ['cspanring@gmail.com'], fail_silently=False)

https://github.com/bancek/django-smtp-ssl

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
The rest of the settings are as per normal:

EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIAIFJGGNCL3QHARMYQ'
EMAIL_HOST_PASSWORD = 'AsY5911gvTIYA6T6drMqDhSt5MPG1leQpvdjA3Rb0sG5'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'MAPC Web App <webapp@mapc.org>'


Server Name:     email-smtp.us-east-1.amazonaws.com
Port:    25, 465 or 587
Use Transport Layer Security (TLS):  Yes


# GeoServer deployment


[DOES NOT START] Jeff recommends using "official" GeoNode GeoServer build:
http://build.geonode.org/geoserver/latest/geoserver.war

[WORKS] Official GeoServer version:
http://downloads.sourceforge.net/geoserver/geoserver-2.2.4-war.zip

GeoNode plugin:
http://build.geonode.org/geoserver/latest/geonode-geoserver-ext-0.3-geoserver-plugin.zip


# Done

* build clean weave db: 
    - weave.* from Verndale
    - gisdata.* from Ubuntu2

    pgdump -Fc -n weave weave.dump
    pgdump -Fc -n gisdata -t public.geometry_columns -t public.spatial_ref_sys gisdata.dump

    pg_restore -d weave weave.dump

    for tbl in `psql -qAt -c "select tablename from pg_tables where schemaname = 'public';" weave` ; do  psql -c "alter table $tbl owner to weave" weave ; done

    users: postgres, weave, django