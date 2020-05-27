from dubbo_client import ApplicationConfig, ZookeeperRegistry, DubboClient, DubboClientError

service_interface = 'com.truthso.monitor.service.CompareService'
registry = ZookeeperRegistry('127.0.0.1:2181')
compare_provider = DubboClient(service_interface, registry, version='1.0.0', group='gaopin')

print(compare_provider.compare({
    u'width': 650,
    u'height': 433,
    u'phash': u'1011100001101000101100001101110101101100101001010101111001001010',
    u'sum': 5429,
    u'ave': 5.0,
    u'dc': 4331,
    u'rSum': 144219,
    u'gSum': 142677,
    u'bSum': 136723,
    u'hash': 4064693128758910538,
}))