import invokust

settings = invokust.create_settings(
    locustfile='../locustfile.py',
    host='https://dss.dev.data.humancellatlas.org/v1/',
    num_requests=10,
    num_clients=1,
    hatch_rate=1
    )

settings.no_reset_stats = False
settings.run_time='30s'
loadtest = invokust.LocustLoadTest(settings)
loadtest.run(timeout=260)
stats = loadtest.stats()
print(stats)