# CZERTAINLY-PyADCS-Connector

> This repository is part of the open-source project CZERTAINLY. You can find more information about the project at [CZERTAINLY](https://github.com/CZERTAINLY/CZERTAINLY) repository, including the contribution guide.

PyADCS `Connector` is the implementation of the following `Function Groups` and `Kinds`:

| Function Group       | Kind           |
|----------------------|----------------|
| `Authority Provider` | `PyADCS-WinRM` |
| `Discovery Provider` | `PyADCS-WinRM` |

PyADCS `Connector` is the implementation of certificate management for Microsoft ADCS that is compatible with the v2 client operations interface. The `Connector` is currently developed to work with through the WinRM protocol.

> It is expected that the SSH PowerShell will be supported in the future.

PyADCS `Connector` allows you to perform the following operations:

`Authority Provider`
- Issue certificate
- Renew certificate
- Revoke certificate

`Discovery Provider`
- Discover certificates

## Database requirements

PyADCS `Connector` requires the PostgreSQL database version 12+.

## Docker container

PyADCS `Connector` is provided as a Docker container. Use the `czertainly/czertainly-pyadcs-connector:tagname` to pull the required image from the repository. It can be configured using the following environment variables:

| Variable                       | Description                                                        | Required                                           | Default value |
|--------------------------------|--------------------------------------------------------------------|----------------------------------------------------|---------------|
| `DATABASE_HOST`                | Database host                                                      | ![](https://img.shields.io/badge/-NO-red.svg)      | `localhost`   |
| `DATABASE_PORT`                | Database port                                                      | ![](https://img.shields.io/badge/-NO-red.svg)      | `5432`        |
| `DATABASE_NAME`                | JDBC URL for database access                                       | ![](https://img.shields.io/badge/-YES-success.svg) | `N/A`         |
| `DATABASE_USER`                | Username to access the database                                    | ![](https://img.shields.io/badge/-YES-success.svg) | `N/A`         |
| `DATABASE_PASSWORD`            | Password to access the database                                    | ![](https://img.shields.io/badge/-YES-success.svg) | `N/A`         |
| `DATABASE_SCHEMA`              | Database schema to use                                             | ![](https://img.shields.io/badge/-NO-red.svg)      | `pyadcs`      |
| `LOG_LEVEL`                    | Logging level, allowed values are `INFO`, `DEBUG`, `ERROR`, `WARN` | ![](https://img.shields.io/badge/-NO-red.svg)      | `INFO`        |
| `ADCS_SEARCH_PAGE_SIZE`        | Number of entries to return in one page                            | ![](https://img.shields.io/badge/-NO-red.svg)      | `500`         |
| `ADCS_ISSUE_POLLING_INTERVAL`  | Interval in milliseconds to poll for issued certificates           | ![](https://img.shields.io/badge/-NO-red.svg)      | `100`         |
| `ADCS_ISSUE_POLLING_TIMEOUT`   | Timeout in milliseconds to wait for issued certificates            | ![](https://img.shields.io/badge/-NO-red.svg)      | `3000`        |
| `ADCS_POOL_MAX_SIZE`           | Maximum size of the connection pool                                | ![](https://img.shields.io/badge/-NO-red.svg)      | `100`         |
| `ADCS_POOL_MIN_WARM_SIZE`      | Minimum size of the warm connection pool                           | ![](https://img.shields.io/badge/-NO-red.svg)      | `10`          |
| `ADCS_POOL_MAX_IDLE_SECONDS`   | Maximum idle time in seconds for the connection pool               | ![](https://img.shields.io/badge/-NO-red.svg)      | `900`         |
| `ADCS_POOL_KEEPALIVE_INTERVAL` | Interval in seconds to keep the connection alive                   | ![](https://img.shields.io/badge/-NO-red.svg)      | `120`         |
