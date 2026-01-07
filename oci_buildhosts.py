import oci

ascend_ocvs_comprtmt = 'ocid1.compartment.oc1..aaaaaaaayb2a6pefrhikvpsyj5quht3gdtjmm4e4kyrkqwvrkmg47554ruhq'

ociconfig = oci.config.from_file("config", "DEFAULT")
hostconfig = oci.ocvp.EsxiHostClient(config=ociconfig)
compute1 = oci.compute.ComputeClient(config=ociconfig)

a =

hosts = hostconfig.list_esxi_hosts(sddc_id='ocid1.vmwaresddc.oc1.uk-london-1.amaaaaaae4ssv6aatxjrniytkxkti37efhgf7sdfy6wstpaey6cffk6krhcq').data

for i in hosts.items:
    if i.lifecycle_state == 'ACTIVE' and i.display_name not in ['ESXi-MGMT-01', 'ESXi-MGMT-02', 'ESXi-MGMT-03']:
        print(i.display_name)