# esxi-exporter
Prometheus exporter, which utilises the VMware SDK to get metrics from VMware ESXi.

## About
This is a prometheus exporter. It collects data of critical services via vCenter from esxi hosts in order to monitor them with prometheus/grafana.

## Getting started

- Simply start the `exporter.py` with python.
- Required information can be passed by environment vars or by commandline arguments

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

**Comandline args**
- `-u` or `--user` the vCenter username
- `-p` or `--password` the vCenter password
- `-o` or `--port` the vCenter port
- `-t` or `--target` the VCenter url without `https://`
- `-w` or `--workers` -1 or 0 is disable, if enabled the ssh queries will be split bitween several python workers 
- `-i` or `--workerid` the id of this worker 
- `-x` or `--noPyVim`  disable pyVmomi service collector
- `-z` or `--noSSH` disable ssh service collector

### SSH Balancing
- The ssh service collector can be split into several docker containers
- If you specify a worker count and a worker id starting by 0 the exporter will slice the available hosts and will only process the specified range wich will result by the hostcount divided by the workercount where the workerid is the index of the slice which will be processed


## Project Structure

**Requirements**
- prometheus-client
- pyVmomi
- Paramiko


## Collectors
- pyVmomni collector collecting servies via vCenter API
- sshCollector collecting missing servies via ssh and multithreading

## What is collected
**sshCollector**
- hostd
- nsx-opsagent
- nsx-proxy
- nsxa
- vvold

**pyVmomiCollector**
- everything vCenter offers
- eg ntp