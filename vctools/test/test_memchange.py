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
import vcloud
from time import sleep

class storeout:
    def __init__(self, key):
        self.actions = {}
        self.key = key
    def save(self, value):
        self.actions[self.key] = value

def test_main():
    """Test routines for dev. Here temporarily"""
    vm_id = 'vm-b8e95c38-b899-496e-bd6b-bcfec39fc52e'
    kvstore = storeout(vm_id)
    boost_thread = vcloud.boost("Boost Thread", vm_id, settings, kvstore)
    boost_thread.start()
    kvstore.actions[vm_id] = ""
    while 1:
        print kvstore.actions[vm_id]
        sleep(0)
    assert 1==1;