# esxi-exporter
Prometheus exporter, which utilises the _VMware SDK_ and _SSH_ to get metrics from _VMware ESXi-HostSystems_.

## About
This exporter contains a `critical service collector` and a `overall state collector`. It monitors the service state of services like `hostd` or `ntpd` and gathers the _ESXi-HostSystem_ `overallState` from _vCenters_. 


## Getting started

1. Configure the project
    - Credentials are passed by environment variables.
    - `config.yaml` contains some static configuration
    - There are command-line options for more console output
2. Run `exporter.py` with _python3_

**Environment variables**
- `VCENTER_USER` the vCenter username
- `VCENTER_PASSWORD` the vCenter password
- `ESXI_USER` the ESXi-host ssh username
- `ESXI_PASSWORD` the ESXi-host ssh password
- `VCENTER_URL` the vCenter url without `https://`

**Command-line arguments**
- `-d` or `--debug` sets logger to debug output
- `-v` or `--info` sets logger to info output
