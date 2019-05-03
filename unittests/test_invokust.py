import invokust

settings = invokust.create_settings(
    locustfile='/home/quokka/data-store-scale-test/locustfile.py',
    host='https://dss.dev.data.humancellatlas.org/v1/',
    num_clients=1,
    hatch_rate=1,
    run_time='30s'
    )

settings.no_reset_stats = False
loadtest = invokust.LocustLoadTest(settings)
loadtest.run()
stats = loadtest.stats()
print(stats)
