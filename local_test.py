import invokust
import json
import tests
import os

os.environ["HOME"] = "/tmp"
os.environ["HCA_CONFIG_FILE"] = "/tmp/config.json"

with open(os.environ["HCA_CONFIG_FILE"], "w") as fh:
    fh.write(json.dumps({}))

settings = invokust.create_settings(
    classes=[tests.SearchUser2],
    host='https://tsmith1.ucsc-cgp-dev.org/v1/',
    num_requests=10,
    num_clients=1,
    hatch_rate=1
    )

loadtest = invokust.LocustLoadTest(settings)
loadtest.run()
print(loadtest.stats())