# esxi-exporter
Prometheus exporter, which utilises the VMware SDK to get metrics from VMware ESXi.

## About
This is a critical service exporter. It uses the vCenter pyVmomi SDK and ssh to retrieve critical services of esxi-hosts in order to monitor them with prometheus.

## Getting started

- Simply start the `exporter.py` with python.
- Required information can be passed by environment variables

**Environment variables**

- `vcenter_user` the vCenter username
- `vcenter_password` the vCenter password
- `vcenter_url` the vCenter url without `https://`
- `exporter_port` the port the exporter should listen on
- `ssh_workercount` the workercount of ssh service collectors
- `ssh_workerid` the id of this worker
- `disable_pyvim` disable pyVmomi service collector
- `disable_ssh` disable ssh service collector
Environments variables can be specified in Linux like this: `export "key"="value"` 
- `netbox_url` the netbox url with `https://`
- `cashtime` cashing the results from netbox for n minutes
- `blacklisttime` when a ssh connection fails you can specify a timespan to blacklist the host in order to avoid locking the user because of too many login attempts 


## Project Structure

### Requirements
- prometheus-client
- pyVmomi
- paramiko
- pynetbox
- requests 


### Collectors
- pyVmomni collector collecting services via vCenter API
- sshCollector collecting missing services via ssh and multithreading

### Problems
- ssh is still required since vCenter does not offer all wanted services.

### Netbox
- We use netbox to double check if a host is really _active_ and ready for use.