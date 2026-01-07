import oci
import datetime
import subprocess
import time

from oci.core.models import AttachIScsiVolumeDetails, MultipathDevice

ascend_ocvs_comprtmt = 'ocid1.compartment.oc1..aaaaaaaayb2a6pefrhikvpsyj5quht3gdtjmm4e4kyrkqwvrkmg47554ruhq'
sddc_id= 'ocid1.vmwaresddc.oc1.uk-london-1.amaaaaaae4ssv6aatxjrniytkxkti37efhgf7sdfy6wstpaey6cffk6krhcq'
bvocid = 'ocid1.volume.oc1.uk-london-1.abwgiljruchllauvsjq3zolwucy7oirlcu4kiaxgkheu7i6dd4b23v3eouwa'
instanceids = []

ociconfig = oci.config.from_file("config", "DEFAULT")
hostclient = oci.ocvp.EsxiHostClient(config=ociconfig)
bvclient = oci.core.BlockstorageClient(config=ociconfig)
comclient = oci.core.ComputeClient(config=ociconfig)
hosts = hostclient.list_esxi_hosts(sddc_id='ocid1.vmwaresddc.oc1.uk-london-1.amaaaaaae4ssv6aatxjrniytkxkti37efhgf7sdfy6wstpaey6cffk6krhcq').data
computelist = comclient.list_instances(compartment_id=ascend_ocvs_comprtmt).data





for i in computelist:
    if i.lifecycle_state == 'RUNNING' and i.display_name in ['ESXi-MGMT-01','ESXi-MGMT-02','ESXi-MGMT-03']:
        attachbvdetails = oci.core.models.AttachVolumeDetails(instance_id=i.id, \
                                                              is_shareable=True, \
                                                              type='iscsi', \
                                                              volume_id=bvocid)

        try:
            attachbv = comclient.attach_volume(attach_volume_details=attachbvdetails).data
            print("Attaching Block Volume to ", i.display_name)
            while attachbv.lifecycle_state != 'ATTACHED':
                attachedins = comclient.get_volume_attachment(volume_attachment_id=attachbv.id).data
                print(i.display_name, attachedins.ipv4)
                attachbv.lifecycle_state = attachedins.lifecycle_state
                time.sleep(15)
        except:
            print(i.display_name, "is already attached")
            getvol = comclient.list_volume_attachments(compartment_id=ascend_ocvs_comprtmt,
                                                       instance_id=i.id).data
            for j in getvol:
                if j.lifecycle_state == 'ATTACHED' and  j.volume_id == bvocid:
                    attachedins1 = comclient.get_volume_attachment(volume_attachment_id=j.id).data
                    print(i.display_name, attachedins1.ipv4, attachedins1.lifecycle_state)






