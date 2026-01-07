
import oci
import datetime
import subprocess
import time
from datetime import timedelta

with open("sessionpub.key.pub", "r") as f:
    content = f.read()
privkeypath = 'C:\\Users\\kdhanusu\\PycharmProjects\\OCI_scripts\\sessionpriv.key'

session_suffix='kdhanusu'
sessionname = 'Session'+str(datetime.datetime.date(datetime.datetime.now()))+session_suffix
ascend_nw_comprtmt='ocid1.compartment.oc1..aaaaaaaakdwqp5fmev7pwri5ynm42eg6ylzaeweqkuto372oosng7kcrmymq'
ascend_ocvs_comprtmt = 'ocid1.compartment.oc1..aaaaaaaayb2a6pefrhikvpsyj5quht3gdtjmm4e4kyrkqwvrkmg47554ruhq'

ociconfig = oci.config.from_file("config", "DEFAULT")
basti = oci.bastion.BastionClient(ociconfig)
bastion = basti.list_bastions(ascend_nw_comprtmt).data[0]
listsession = basti.list_sessions(bastion.id).data

sessiondetails = oci.bastion.models.CreateSessionDetails( \
    display_name = sessionname, \
    bastion_id = bastion.id, \
    target_resource_details = oci.bastion.models.CreateDynamicPortForwardingSessionTargetResourceDetails(session_type="DYNAMIC_PORT_FORWARDING"), \
    key_type = 'PUB', \
    key_details = oci.bastion.models.PublicKeyDetails(public_key_content=content), \
    session_ttl_in_seconds = 10700)


for i in listsession:
    if i.lifecycle_state == 'ACTIVE' and session_suffix in i.display_name:
        deletesession = basti.delete_session(i.id).data
        print("Old session is deleted")

while True:
    print("Creating a New Bastion Session")
    createsesion = basti.create_session(sessiondetails).data
    while createsesion.lifecycle_state != 'ACTIVE':
        getseson = basti.get_session(createsesion.id).data
        createsesion.lifecycle_state = getseson.lifecycle_state
        time.sleep(20)
    print("Bastion session is Active")
    ssh_cmd = "ssh -i " + privkeypath + " -N -D 127.0.0.1:1080 -p 22 "+ createsesion.id+"@host.bastion."+ociconfig['region']+'.oci.oraclecloud.com'
    ssh_process = subprocess.run(ssh_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10500)
    deletesession = basti.delete_session(createsesion.id).data
    print("Bastion session is deleted")