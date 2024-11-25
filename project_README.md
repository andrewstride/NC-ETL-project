# TerrificTotes Data Lakehouse Project

This project is a data lakehouse, that takes data from an OLTP database (ToteSys), transforms it into a star-schema format, and places it within a OLAP data warehouse.

The project has **two S3 buckets** - an ingestion bucket and a processing bucket.

It also contains **three Lambdas**...
- **Lambda1** - takes data from the OLTP ToteSys database, and places it as raw data, in csv format, in the ingestionb bucket.
- **Lambda2** - takes data from the ingestion bucket, transforms it into star-schema format, and places it, as parquet format, in the processing bucket.
- **Lambda3** - takes data from the processing bucket and places it within the OLAP data warehouse.

## Usage

There are several make commands that can be run when using the project...

- **make create-environment** - creates a virtual environment.
- **make requirements** - downloads the relevant dependencies for the project.
- **make dev-setup** - sets up dev requirements (bandit, pip-audit, black).
- **make run-checks** - runs checks on the project code (security test, black, unit tests, and coverage checks)
- **make layer-setup** - prepare the lambda layers.
- **make clean** - clean up the lambda layer dependencies.
- **make all** - run all of the commands.

