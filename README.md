# CZERTAINLY-PyADCS-Connector

Using Python 3.12.

## Docker container

PyADCS `Connector` is provided as a Docker container. Use the `harbor.3key.company/czertainly/czertainly-pyadcs-connector:tagname` to pull the required image from the repository. It can be configured using the following environment variables:

| Variable                | Description                                                        | Required                                           | Default value |
|-------------------------|--------------------------------------------------------------------|----------------------------------------------------|---------------|
| `DATABASE_HOST`         | Database host                                                      | ![](https://img.shields.io/badge/-NO-red.svg)      | `localhost`   |
| `DATABASE_PORT`         | Database port                                                      | ![](https://img.shields.io/badge/-NO-red.svg)      | `5432`        |
| `DATABASE_NAME`         | JDBC URL for database access                                       | ![](https://img.shields.io/badge/-YES-success.svg) | `N/A`         |
| `DATABASE_USER`         | Username to access the database                                    | ![](https://img.shields.io/badge/-YES-success.svg) | `N/A`         |
| `DATABASE_PASSWORD`     | Password to access the database                                    | ![](https://img.shields.io/badge/-YES-success.svg) | `N/A`         |
| `DATABASE_SCHEMA`       | Database schema to use                                             | ![](https://img.shields.io/badge/-NO-red.svg)      | `pyadcs`      |
| `LOG_LEVEL`             | Logging level, allowed values are `INFO`, `DEBUG`, `ERROR`, `WARN` | ![](https://img.shields.io/badge/-NO-red.svg)      | `INFO`        |
| `ADCS_SEARCH_PAGE_SIZE` | Number of entries to return in one page                            | ![](https://img.shields.io/badge/-NO-red.svg)      | `500`         |