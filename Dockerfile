# Dockerfile
FROM python:3.12-alpine as common-base

ENV DJANGO_SETTINGS_MODULE=CZERTAINLY_PyADCS_Connector.settings
ENV PYTHONUNBUFFERED=1

RUN apk update && \
  apk add --no-cache gcc python3-dev krb5-dev openssl-dev libffi-dev

FROM common-base as base-builder

RUN pip install -U pip setuptools
RUN mkdir -p /app
WORKDIR /app

# Stage 1: Extract dependency information from setup.py alone
# Allows docker caching until setup.py changes
FROM base-builder as dependencies

COPY django-PyADCSConnector /app
RUN python setup.py egg_info

# Stage 2: Install dependencies based on the information extracted from the previous step
# Caveat: Expects an empty line between base dependencies and extras, doesn't install extras
# Also installs gunicon in the same step
FROM base-builder as builder

RUN apk update && apk add --no-cache build-base python3-dev
RUN mkdir -p /install

COPY --from=dependencies /app/django_PyADCSConnector.egg-info/requires.txt /tmp/
RUN sh -c 'pip install --no-warn-script-location --prefix=/install $(grep -e ^$ -m 1 -B 9999 /tmp/requires.txt) gunicorn'
# Everything up to here should be fully cacheable unless dependencies change
# Now copy the application code
COPY django-PyADCSConnector /app
COPY ./CZERTAINLY_PyADCS_Connector /app
# Stage 3: Install application
RUN sh -c 'pip install --no-warn-script-location --prefix=/install .'

# Stage 4: Install application into a temporary container, in order to have both source and compiled files
# Compile static assets
FROM builder as static-builder
RUN cp -r /install/* /usr/local
#RUN sh -c 'python manage.py collectstatic --no-input'

# Stage 5: Install compiled static assets and support files into clean image
FROM common-base

# add non root user czertainly
RUN addgroup --system --gid 10001 czertainly && adduser --system --home /opt/czertainly --uid 10001 --ingroup czertainly czertainly

COPY docker /
RUN mkdir -p /opt/czertainly

COPY --from=builder /install /usr/local
#COPY --from=static-builder /app/static.dist /app/static.dist

WORKDIR /opt/czertainly

EXPOSE 8080

USER 10001

ENTRYPOINT ["/opt/czertainly/entry.sh"]
