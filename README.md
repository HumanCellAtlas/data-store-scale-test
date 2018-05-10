# HCA DSS: Scalability Tests

This is a suite of scalability tests for the [Data Storage System](github.com/HumanCellAtlas/data-store), which is the 
storage platform used by the [Human Cell Atlas](https://www.humancellatlas.org/).
 

The tests use [locust](https://docs.locust.io/en/stable/what-is-locust.html) the load testing framework.

[locust-cloudwatch](https://www.concurrencylabs.com/blog/how-to-export-locust-metrics-to-cloudwatch/) for adding logs to cloudwatch.
[locust-docker](https://github.com/sernst/locusts) image.
[Docker Locust](https://github.com/zalando-incubator/docker-locust)
[How do I Loucst](https://github.com/pglass/how-do-i-locust)

#### About the scalability testing framework

- [Centralised logging for AWS Lambda]https://hackernoon.com/centralised-logging-for-aws-lambda-b765b7ca9152
- different ways to scale out
    - [AWS Lambdas](https://github.com/FutureSharks/invokust)
    - [AWS Elastic Beanstalk](https://aws.amazon.com/blogs/devops/using-locust-on-aws-elastic-beanstalk-for-distributed-load-generation-and-testing/)
    - [Docker Swarm](https://wheniwork.engineering/load-testing-with-locust-io-docker-swarm-d78a2602997a)
    
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

#### Modifying the Tests
You can adjust the way the load test runs by modifying `DSS-scalability/locustfile.py`. 

Additional test should be added to `Dss-scalability/locustfiles.py` and imported into `DSS-scalability/locustfile.py`.

#### Adding new requirements
If new python module is required, added the requirement to `DSS-scalability/requirements.txt`. 

If  using Elasticbeanstock add the new requirements to `DSS-scalability/eb-locustio-sample/.ebextensions/setup.config`
under `locust36`.


