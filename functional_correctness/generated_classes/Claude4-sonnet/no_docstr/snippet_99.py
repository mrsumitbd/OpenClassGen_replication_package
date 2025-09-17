class VmDetailsCommand(object):

    def __init__(self, pyvmomi_service, vm_details_provider):
        self.pyvmomi_service = pyvmomi_service
        self.vm_details_provider = vm_details_provider

    def get_vm_details(self, si, logger, resource_context, requests, cancellation_context):
        results = []
        for request in requests:
            try:
                vm = self.pyvmomi_service.find_vm_by_name(si, request.vm_name)
                if vm is None:
                    results.append(None)
                    continue
                
                self._wait_for_vm_to_be_ready(vm, request, logger)
                
                if cancellation_context.is_cancelled:
                    break
                
                vm_details = self.vm_details_provider.get_vm_details(vm, request)
                results.append(vm_details)
                
            except Exception as e:
                logger.error(f"Error getting VM details for {request.vm_name}: {str(e)}")
                results.append(None)
        
        return results

    def _wait_for_vm_to_be_ready(self, vm, request, logger):
        import time
        timeout = getattr(request, 'timeout', 300)
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if vm.runtime.powerState == 'poweredOn':
                if not self._not_guest_net(vm) and not self._no_guest_ip(vm, request):
                    return
            time.sleep(5)
        
        logger.warning(f"VM {vm.name} did not become ready within timeout period")

    @staticmethod
    def _not_guest_net(vm):
        try:
            return vm.guest.net is None or len(vm.guest.net) == 0
        except:
            return True

    @staticmethod
    def _no_guest_ip(vm, request):
        try:
            if vm.guest.net:
                for net in vm.guest.net:
                    if net.ipAddress:
                        for ip in net.ipAddress:
                            if ip and not ip.startswith('169.254'):
                                return False
            return True
        except:
            return True