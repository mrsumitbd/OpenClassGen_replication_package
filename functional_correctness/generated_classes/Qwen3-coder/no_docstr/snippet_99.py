class VmDetailsCommand(object):
    def __init__(self, pyvmomi_service, vm_details_provider):
        self.pyvmomi_service = pyvmomi_service
        self.vm_details_provider = vm_details_provider

    def get_vm_details(self, si, logger, resource_context, requests, cancellation_context):
        results = []
        
        for request in requests:
            if cancellation_context.is_cancelled:
                break
                
            try:
                vm = self.pyvmomi_service.find_by_uuid(si, request.vm_uuid)
                if not vm:
                    results.append({"error": f"VM with UUID {request.vm_uuid} not found"})
                    continue
                    
                # Wait for VM to be ready
                if not self._wait_for_vm_to_be_ready(vm, request, logger):
                    results.append({"error": f"VM {request.vm_uuid} is not ready"})
                    continue
                
                # Get VM details
                vm_details = self.vm_details_provider.get_vm_details(vm, resource_context, request)
                results.append(vm_details)
                
            except Exception as e:
                logger.error(f"Error getting details for VM {request.vm_uuid}: {str(e)}")
                results.append({"error": str(e)})
                
        return results

    def _wait_for_vm_to_be_ready(self, vm, request, logger):
        # Check if VM is powered on
        if vm.runtime.powerState != 'poweredOn':
            return False
            
        # Check for guest networking
        if self._not_guest_net(vm):
            return False
            
        # Check for guest IP
        if self._no_guest_ip(vm, request):
            return False
            
        return True

    @staticmethod
    def _not_guest_net(vm):
        return not vm.guest.net

    @staticmethod
    def _no_guest_ip(vm, request):
        if not vm.guest.net:
            return True
            
        # Check if any interface has an IP
        for net in vm.guest.net:
            if net.ipConfig and net.ipConfig.ipAddress:
                return False
                
        return True