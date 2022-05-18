# shell-v
Scripts written in bash and python to help make light work of Vault interactions.

## Vault Probe
Python script to output information about a HashiCorp Vault instance

### Usage
```bash
export VAULT_ADDR=my-vault.com:8200
export VAULT_CACERT=/opt/vault/tls/vault-ca.pem
export VAULT_TOKEN=hvs.89dsa76a5sd8a9as98d7asd7	# needs to have sufficient rights over the cluster; do not use the root token
./hc-vault-probe.sh -h
```
The VAULT_ADDR address should point at the layer 4 load balancer for the cluster so that the report is from the perspective of the active leader node.
Some values are not yet process, such as client count and lease processing.

## Help File

```shell
usage: hc-vault-probe.py [-h] [-s] [-n NAMESPACE] [-q]

HashiCorp Vault Enterprise probe, for convenient iteration of enterprise namespaces for rudimentary reporting

To just output information about the system as a whole:
  -s, --system                         Output information about the system as a whole, not namespaces-level information

Focus output to a specific namespace:
  -n NAMESPACE, --namespace NAMESPACE  Specify a namespace to operate on; use the string all for all namespaces on the system

Hide dressing for better pipeline work:
  -q, --quiet                          Hide extraneous output

optional arguments:
  -h, --help                           show this help message and exit
```

## Official Statement

By using the software in this repository (the “Software”), you acknowledge that: (1) the Software is still in development, may change, and has not been released as a commercial product by HashiCorp and is not currently supported in any way by HashiCorp; (2) the Software is provided on an “as-is” basis, and may include bugs, errors, or other issues; (3) the Software is NOT INTENDED FOR PRODUCTION USE, use of the Software may result in unexpected results, loss of data, or other unexpected results, and HashiCorp disclaims any and all liability resulting from use of the Software; and (4) HashiCorp reserves all rights to make all decisions about the features, functionality and commercial release (or non-release) of the Software, at any time and without any obligation or liability whatsoever.
