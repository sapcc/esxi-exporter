import logging
from os import getenv
from queue import Queue
from threading import Thread

from prometheus_client.core import GaugeMetricFamily

from BaseCollector import BaseCollector

# init logging
logger = logging.getLogger('esxi-exporter')


class EsxiOnlineStateCollector(BaseCollector):

    def __init__(self) -> None:
        super().__init__()

    def worker(q: Queue, output: dict):
        while not q.empty():
            host = q.get()
            output[host.name] = host.overallStatus

    def collect(self):

        gauge_metric = GaugeMetricFamily('esxi_overall_state', '0=unknown 1=red, 2=orange, 3=green',
                                         labels=['vcenter', 'hostsystem'])

        # get all hosts from vcenter
        vc_hosts = self.get_vcenter_hosts()

        # prepare multithreading
        threads = []
        results = {}
        q = Queue()
        [q.put(host) for host in vc_hosts]

        for i in range(getenv('vc_workercount', 10)):
            t = Thread(target=EsxiOnlineStateCollector.worker, args=(q, results))
            threads.append(t)
            t.start()

        [t.join() for t in threads]

        # parse results
        for host, value in results.items():
            if value == 'green':
                state = 3
            elif value == 'yellow':
                state = 2
            elif value == 'red':
                state = 1
            else:
                state = 0
            gauge_metric.add_metric(labels=[getenv('vcenter_url'), host, 'ssh_connection'], value=state)

        yield gauge_metric
