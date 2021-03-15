# esxi-exporter
Prometheus exporter, which utilises the VMware SDK to get metrics from VMware ESXi.

## About
This is a critical service exporter. It uses the vCenter pyVmomi SDK and ssh to retrieve critical services of esxi-hosts in order to monitor them with prometheus.
The term services relates to linux-services like `hostd` or `ntp`. Esxi means esxi-hostsystem.

## Getting started

- Required information can be passed by environment variables
- Environments variables can be specified in Linux like this: `export "key"="value"` 
- Simply start the `exporter.py` with python.

**Environment variables**
- `VCENTER_USER` the vCenter username - required
- `VCENTER_PASSWORD` the vCenter password - required
- `VCENTER_URL` the vCenter url without `https://` - required
- `EXPORTER_PORT` the port the exporter should listen on - default: 1234 
- `SSH_WORKERCOUNT` the workercount of ssh service collectors - default: 10
- `VC_WORKERCOUNT` the workercount of esxi overall state collectors - default: 10
- `DISABLE_PYVIM` disable pyVmomi service collector - optional, 0 or 1
- `DISABLE_SSH` disable ssh service collector - optional, 0 or 1
- `DISABLE_OVERALLSTATE` disable esxi overall state collector - optional, 0 or 1
- `NETBOX_URL` the netbox url with `https://` - required
- `CASHTIME` cashing the results from netbox for n minutes - default 60min
- `BLACKLISTTIME` when a ssh connection fails you can specify a timespan to blacklist the host in order to avoid locking the user because of too many login attempts - default 20 min 

## Changing monitored services
- This regards to the ssh-collector
- Open the `SshServiceCollector` file in the `collectors` folder
- Modify the following line:


```python
self._monitoredServices = [
    'hostd', 'nsx-opsagent', 'nsx-proxy', 'nsxa', 'ntpd', 'vpxa', 'vvold']
```

### Recomendation
- The current approch is to disable the `pyVimServiceCollector` since it does not offer all services of interest and the ssh approach works pretty fast (200 esxi in 30sec) as long as there are not too many services to be monitored. So all load belongs to the ssh service collector. 


## Project Structure

### Requirements
- prometheus-client
- pyVmomi
- paramiko
- pynetbox
- requests 


### Collectors
- _pyVmomni service collector_: utilising pyVmomi to get services of esxi-hostsystems from vCenter. Does not return all services of interest. 
- _ssh service Collector_: collecting missing services via ssh and multithreading
- _esxi overall state collector_: collecting vCenter "overallstate" of esxi-hostsystems

### Problems
- ssh is still required since vCenter does not offer all wanted services.

### Netbox
- We use netbox to double check if a host is really _active_ and ready for use.