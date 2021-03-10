# esxi-exporter
Prometheus exporter, which utilises the VMware SDK to get metrics from VMware ESXi.

## About
This is a critical service exporter. It uses the vCenter pyVmomi SDK and ssh to retrieve critical services of esxi-hosts in order to monitor them with prometheus.

## Getting started

- Simply start the `exporter.py` with python.
- Required information can be passed by environment variables or by command-line arguments

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

**Comandline arguments**

- `-u` or `--user` the vCenter username
- `-p` or `--password` the vCenter password
- `-o` or `--port` the vCenter port
- `-t` or `--target` the VCenter url without `https://`
- `-w` or `--workers` -1 or 0 is disable, if enabled the ssh queries will be split between several python workers 
- `-i` or `--workerid` the id of this worker 
- `-x` or `--noPyVim`  disable pyVmomi service collector
- `-z` or `--noSSH` disable ssh service collector
- `-n` or `--netbox_url` the netbox url with `https://`
- `-j` or `--cashtime` cashing the results from netbox for n minutes
- `-i` or `--blacklisttime` when a ssh connection fails you can specify a timespan to blacklist the host in order to avoid locking the user because of too many login attempts 





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

### Problem
- Sadly vCenter does not offer all services we need. So we still have to use ssh.

### Netbox
- We use netbox to double check if a host is really _active_ and ready for use.