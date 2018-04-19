# HCA DSS: Scalability Tests

This is a suite of scalability tests for the [Data Storage System](github.com/HumanCellAtlas/data-store), which is the 
storage platform used by the [Human Cell Atlas](https://www.humancellatlas.org/).
 

The tests use [locust](https://docs.locust.io/en/stable/what-is-locust.html) the load testing framework and [invokust](https://github.com/FutureSharks/invokust)
to run the tests using [AWS Lambdas](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html).

#### About the scalability testing framework



#### Running the scale test locally

- make it run from command line. Take host as a parameter
- deploy dashboards if you have permission. Do this in DSS repo.
- deploy lambdas using make deploy
- setup environment variables

#### Adding new tests


