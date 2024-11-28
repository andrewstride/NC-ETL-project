# TerrificTotes Data platform Project

## Introduction

This project creates a data platform, that **extracts** data from an operational (OLTP) database (called ToteSys), **transforms** it into a star-schema format, stores in a data lake, and **loads** it within a OLAP data warehouse.

## About

The project has **two S3 buckets** - an ingestion bucket and a processing bucket.

It also contains **three Lambdas**...

- **Lambda1** - extracts data from the OLTP ToteSys database, and places it as raw data, in csv format, in the ingestion bucket.
- **Lambda2** - takes data from the ingestion bucket, transforms it into star-schema format, and places it, as parquet format, in the processing bucket.
- **Lambda3** - takes data from the processing bucket and loads it within the OLAP data warehouse.

The Lambdas also has **CloudWatch alerts**, and if a serious alert is triggered (an **email** is sent to: <TheTerraformers@protonmail.com>).

## Visual Diagram

![image](https://github.com/user-attachments/assets/c33c64f2-a473-420a-aa45-033201c809b8)



**Brief** - Diagram depicting the internal workings and structure of the project.

## Developer Instructions

These instructions are geared towards the **contributors** (*how to build and install the application **locally***).

- **Running The Make File**

    There are several make commands that can be run when using the project...

  - **make create-environment** - creates a virtual environment.
  - **make requirements** - downloads the relevant dependencies for the project.
  - **make dev-setup** - sets up dev requirements (*bandit, pip-audit, black*).
  - **make run-checks** - runs checks on the project code (*security test, black, unit tests, and coverage checks*)
  - **make layer-setup** - prepare the lambda layers.
  - **make clean** - clean up the lambda layer dependencies.
  - **make notebook** - starts up the Jupyter notebook environment for data analysis
  - **make all** - run all of the commands.

    Be sure to double check for sake of ensuring these commands are being executed within a contained virtual environment.

- **Accessing Totesys database**

  - Database is being operated from a remote server in which appropriate access credentials will be required.

  - The database contents can be retrieved using the access credentials provided by the project admin (*please contact your team admin if not yet received access credential*).

- **Environment Variables Required**

  A dotenv file will need to be created in order to house your access credentials used for connection to the database (*This should be included in your gitignore file by any means necessary*).

- **Testing**

  Testing connections and util functions using the the test suit provided.

  - This shout be done using the pytest libraries available along with some elements of unit testing used throughout the test suit (*No entries are eligible for merger without thoro testing accompanied*).

- **Making Pull Requests**

  When making a pull request here is how it should be done in regards to the current data platform application specifically...

  - After you have liaised with fellow operatives (*one or more*) a pull request is then eligible for submission (*considering it meets all eligibility criteria*).

  - The pull request will then be examined in further detail by another member of the group (*one or more*) were it will then be approved or refused (*during this time a comment will be made specifying the reasons for an approved or refused submission*).

  - Successful submissions will then go on to be merged by the group admin.

  - Unsuccessful submissions will have specifics as to why attached to the refusal note in the comment section and further addressing of the area mentioned there in is encouraged.

  Please do not be discouraged by any refusal of submissions and further submissions are encouraged throughout the lifecycle of the project in question.

## Expectations For Contributors

Contributors to the project in question are expected to...

- Be sure to create a separate branch before editing or adding of any functionality to any features currently in use on the main branch of the repository.

- Alert fellow developers when any changes have been merged to main to aid in the prevention of any merge conflicts that could occur later in project dealings when meeting deadlines (*announce a new push and or merger in the slack channel provided*).

- Code is thoroughly tested using pytest and elements of unittest before submission for merger.

- Code is heavily scrutinized during review process before approval or denial.

- If a pull request is refused please specify what the reasons were that brought forth this decision for the benefit of all fellow developers understanding.

- Any difficulty understanding feature functionality should be reported to admin for a timely response within 24 hours providing clarity (*if the logistics have become clear before a response is given please make aware in a follow up message to the team admin*).

- Any additional library imports should be added to your branches requirements text file along with a brief comment (*In requirements*) specifying the need for said import (*If import is deemed unfit for any reason a removal of said import may be requested or a pull request may be refused in its entirety due to said import*).

## List of Known Issues

...
