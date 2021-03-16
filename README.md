# esxi-exporter
Prometheus exporter, which utilises the VMware SDK to get metrics from VMware ESXi.

## About
This is a critical service exporter. It uses the vCenter pyVmomi SDK and ssh to retrieve critical services of esxi-hosts in order to monitor them with prometheus.
The term services relates to linux-services like `hostd` or `ntp`. ESXi means esxi-hostsystem.


## Getting started

- Required information can be passed by environment variables
- Environments variables can be specified in Linux like this: `export "key"="value"` 
- Simply start the `exporter.py` with python.

**Environment variables**
- `VCENTER_USER` the vCenter username - required
- `VCENTER_PASSWORD` the vCenter password - required
- `ESXI_USER` the ESXi-host ssh username - required
- `ESXI_PASSWORD` the ESXi-host ssh password - required
- `VCENTER_URL` the vCenter url without `https://` - required
- `NETBOX_URL` the netbox url with `https://` - required

**Command-line arguments**
- `-d` or `--debug` sets logger to debug output
- `-v` or `--info` sets logger to info output


### Configuration
- Open the `config yaml.`
- If you enable collectors ensure that the classname matches the filename.
### Recomendation
- The current approch is to disable the `pyVimServiceCollector` since it does not offer all services of interest and the ssh approach works pretty fast (200 esxi in 30sec) as long as there are not too many services to be monitored. So all load belongs to the ssh service collector. 


## Project Structure

### Collectors
- _pyVmomni service collector_: utilising pyVmomi to get services of esxi-hostsystems from vCenter. Does not return all services of interest. 
- _ssh service Collector_: collecting missing services via ssh and multithreading
- _esxi overall state collector_: collecting vCenter "overall_state" of esxi-hostsystems

### Problems
- ssh is still required since vCenter does not offer all wanted services.

### Netbox
- We use netbox to double check if a host is really _active_ and ready for use.
