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
- `vcenter_user` the vCenter username - required
- `vcenter_password` the vCenter password - required
- `vcenter_url` the vCenter url without `https://` - required
- `exporter_port` the port the exporter should listen on - default: 1234 
- `ssh_workercount` the workercount of ssh service collectors - default: 10
- `vc_workercount` the workercount of esxi overall state collectors - default: 10
- `disable_pyvim` disable pyVmomi service collector - optional, 0 or 1
- `disable_ssh` disable ssh service collector - optional, 0 or 1
- `disable_overallstate` disable esxi overall state collector - optional, 0 or 1
- `netbox_url` the netbox url with `https://` - required
- `cashtime` cashing the results from netbox for n minutes - default 60min
- `blacklisttime` when a ssh connection fails you can specify a timespan to blacklist the host in order to avoid locking the user because of too many login attempts - default 20 min 

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