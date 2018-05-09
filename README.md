# HCA DSS: Scalability Tests

This is a suite of scalability tests for the [Data Storage System](github.com/HumanCellAtlas/data-store), which is the 
storage platform used by the [Human Cell Atlas](https://www.humancellatlas.org/).
 

The tests use [locust](https://docs.locust.io/en/stable/what-is-locust.html) the load testing framework.

[locust-cloudwatch](https://github.com/concurrencylabs/locust-cloudwatch) for adding logs to cloudwatch.
[locust-docker](https://github.com/sernst/locusts) image.

#### About the scalability testing framework



#### Running the scale test locally
- configure locust.config.json with the host and the Users to run.
- copy locustfiles to ./scripts directory.
- `docker build -t loctest .`
- `docker run -it --rm -v ~/workspace/DSS-scalability/scripts:/scripts loctest`

- Build docker image
- make it run from command line. Take host as a parameter
- deploy dashboards if you have permission. Do this in DSS repo.
- deploy lambdas using make deploy
- setup environment variables

#### Adding new tests


