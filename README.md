# HCA DSS: Scalability Tests

This is a suite of scalability tests for the [Data Storage System](https://github.com/HumanCellAtlas/data-store/), which is the storage platform used by the [Human Cell Atlas](https://www.humancellatlas.org/).

The tests use [locust](https://docs.locust.io/en/stable/what-is-locust.html) the load testing framework. Here are some
resources for working with locust.
- [locust-cloudwatch](https://www.concurrencylabs.com/blog/how-to-export-locust-metrics-to-cloudwatch/) for adding
locust metrics to cloudwatch.
- A [locust-docker](https://github.com/sernst/locusts) image.
- A more advanced [Docker Locust](https://github.com/zalando-incubator/docker-locust) image
- Tips on [How do I Loucst](https://github.com/pglass/how-do-i-locust)

#### About the scalability testing framework
- different ways to scale out
    - [AWS Lambdas](https://github.com/FutureSharks/invokust)
    - [AWS Elastic Beanstalk](https://aws.amazon.com/blogs/devops/using-locust-on-aws-elastic-beanstalk-for-distributed-load-generation-and-testing/)
    - [Docker Swarm](https://wheniwork.engineering/load-testing-with-locust-io-docker-swarm-d78a2602997a)

#### Running the scale test locally

To run using docker you:
- configure `DSS-scalability/locust-docker/locust.config.json` with the host and the Users to run.
- copy `DSS-scalability/locustfiles` to `DSS-scalability/locust-docker/scripts` directory.
- run `docker build -t loctest .`
- run `docker run -it --rm -v ./DSS-scalability/scripts:/scripts loctest`

- Build docker image
- make it run from command line. Take host as a parameter
- deploy dashboards if you have permission. Do this in DSS repo.
- deploy lambdas using make deploy
- setup environment variables

#### Running from CLI

Using Python 3.6:

    $ pip install -r requirements.txt
    $ locust -f ./scale_tests/upload_cloud.py --host=$HOST --no-web --client=100 --hatch-rate=50 --run-time=10s --csv=./scale_tests/upload

Where `$HOST` is the base URL of the DSS endpoint you want to hit, e.g. `https://dss.dev.data.humancellatlas.org/v1/`. (The tests will look for `${HOST}swagger.yaml`.)

#### Environment Variables
- `TARGET_URL` - specifies the endpoint for unittests to target (e.g. `https://dss.dev.data.humancellatlas.org/v1/`).
- `GOOGLE_APPLICATION_CREDENTIALS` - A file path to google application credentials Used to access endpoints that require Auth.

#### Modifying the Tests
Preconfigured test are located in `./scale_tests`. Additional scale test should be added to this directory.

#### Adding new requirements
If new python module is required, added the requirement to `DSS-scalability/requirements.txt`.

If using Elastic Beanstalk add the new requirements to `DSS-scalability/eb-locustio-sample/.ebextensions/setup.config`
under `locust36`.


##### Update chalice requirements
downloads the packages for aws lambda env

    docker run -it --volume=$PWD:/pp python:3.6 bash -c "pip download invokust locustio==0.8.1 gevent==1.2.2 git+git://github.com/HumanCellAtlas/dcp-cli#egg=hca --dest=/pp"

How to build _wheels_ for the aws lambda env
1. Run `docker run -it --volume=$PWD:/chalice python:3.6 bash -c “pip wheel —wheel-dir=chalice/py_pkgs -r /requirements.txt"`
1. follow instructions after "The cryptography wheel file has been built" -> [chalice requirements example](https://chalice.readthedocs.io/en/latest/topics/packaging.html?highlight=requirements)


#### Known issues

Some macOS users might see an error like:

    Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known

This is because newer version of macOS impose a much stricter limit on the maximum
amount of open file descriptors. This issue can be addressed by doing

    $ ulimit -S -n 10240

before running tests, which should increase the open file descriptor limit to 10240 until the
next reboot.
