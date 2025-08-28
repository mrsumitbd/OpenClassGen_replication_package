class VmDetailsCommand(object):

    def __init__(self, pyvmomi_service, vm_details_provider):
        self.pyvmomi_service = pyvmomi_service
        self.vm_details_provider = vm_details_provider

    def get_vm_details(self, si, logger, resource_context, requests, cancellation_context):
        """
        Retrieves VM details for each request object in `requests`.
        Returns a list of detail dicts, one per request.
        """
        # Locate the VM by its managed object ID (moid)
        vm = self.pyvmomi_service.get_vm_by_moid(si, resource_context.resource_id)
        results = []
        for req in requests:
            # If the request wants to wait for an IP, block until ready
            if getattr(req, "wait_for_ip", False):
                self._wait_for_vm_to_be_ready(vm, req, logger)
            # Delegate to provider to fetch the actual details
            detail = self.vm_details_provider.get_vm_details(vm, req)
            results.append(detail)
        return results

    def _wait_for_vm_to_be_ready(self, vm, request, logger):
        """
        Polls the VM guest properties until it has network adapters
        and at least one IP of the requested type (if specified).
        """
        timeout = getattr(request, "timeout_seconds", 300)
        interval = getattr(request, "poll_interval_seconds", 5)
        start = time.time()
        while True:
            if cancellation_event := getattr(request, "cancellation_event", None):
                if cancellation_event.is_set():
                    raise Exception("Operation cancelled while waiting for VM network readiness")
            # Check for presence of guest.net and guest IPs
            if not self._not_guest_net(vm) and not self._no_guest_ip(vm, request):
                return
            elapsed = time.time() - start
            if elapsed >= timeout:
                raise Exception(f"Timeout ({timeout}s) waiting for VM '{vm.name}' network/IP readiness")
            logger.info(
                f"Waiting for VM '{vm.name}' to report networks and IP (waited {int(elapsed)}s)..."
            )
            time.sleep(interval)

    @staticmethod
    def _not_guest_net(vm):
        """
        Returns True if vm.guest.net is empty or missing.
        """
        try:
            nets = vm.guest.net
        except AttributeError:
            return True
        return not bool(nets)

    @staticmethod
    def _no_guest_ip(vm, request):
        """
        Returns True if the VM has no guest IP matching the request criteria.
        If request.ip_type is set to 'ipv4' or 'ipv6', filters accordingly.
        """
        ip_type = getattr(request, "ip_type", None)
        try:
            nets = vm.guest.net or []
        except AttributeError:
            return True

        for net in nets:
            addrs = getattr(net, "ipAddress", None) or []
            for addr in addrs:
                if not addr:
                    continue
                if ip_type:
                    # crude check: IPv4 contains dots, IPv6 contains colons
                    if ip_type.lower() == "ipv4" and "." in addr:
                        return False
                    if ip_type.lower() == "ipv6" and ":" in addr:
                        return False
                else:
                    return False
        return True