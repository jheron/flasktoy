# feflask - trivial front end flask app

The application is a trivial flask project which connects to a postgres database named postgres. The credentials are embedded into the app which would need to be factored out in production.

## Deployment artifacts

Application images are provided in 2 basic flavors:

1. tar.gz uploaded to s3 which contain the application. When untar'd these are in a directory with a python virtual env which includes any external libraries or dependencies. These are named like feflask-$OS_$VERSION. A shasum file is provided to allow integrity checking. Each image is produced for rhel6, rhel7, sl6, sl7, centos6 and centos7. They can be downloaded to a flash drive or other removale media for loading into airgapped systems.

2. self contained docker images saved into tar.gz files. Like non-docker distribution there is a shasum and they also come in rhel6, rhel7, sl6, sl7, centos6 and centos7 flavors.

## Tests

There are unit and functional tests. Like the application they are also trivial although the functional test uses an REST-like http api named /health which also checks that the database is available. The tests provide junit style xml output.

In addition there is a standalone script for testing database connectivity.

## CI/CD

Jenkins pipeline configured to kick off with a githook on checkin using PollSCM (jenkins not visible to github).

The Jenkins pipeline builds and tests the app by calling a Makefile which uses docker to build the app.

Semantic versioning is implemented using bumpversion on commit.

## TODO

* Complete build system testing.
* Add tar.gz test to Makefile
* Move CI/CD build and test environment onto physicals or cloud.
* Get app and database into a docker stack so we can take better advantage of secret handling or alternatively find a better more general mechanism for managing secrets.
* Configure jenkins in docker.
* Fix a problem with the naming of images for sl6 and sl7.
