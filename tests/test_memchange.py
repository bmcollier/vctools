"""Python vCloud API Interface Test - Memchange

Desired behaviour:

We begin by getting the memory settings on a VM.
We then shutdown the machine remotely, and wait for this process to finish.
We then change the memory settings and wait for a signal that the change has completed.
We then activate the machine again.
We then check that the machine is reporting its memory correctly (ie. the new value).

"""
from pytest import raises
from vcloud_settings import settings

def test_1():
    """Test routines for dev. Here temporarily"""
    vc_session = VCloudSession(settings.username, settings.password, settings.organisation, settings.endpoint)
    print vc_session.last_status
    print vc_session.organisation_url()
    print vc_session.get_vapp('vapp-a88887a3-a15f-4f11-8482-993159b33ad8')
    #print vc_session.suspend_vapp('vapp-a88887a3-a15f-4f11-8482-993159b33ad8')
    #print vc_session.set_memory_config('vm-b8e95c38-b899-496e-bd6b-bcfec39fc52e')
    assert 1==1;