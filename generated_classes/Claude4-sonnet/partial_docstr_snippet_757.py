class CpcSetAutoStartListHandler:
    '''
    Handler class for operation: Set Auto-start List.
    '''

    @staticmethod
    def post(method, hmc, uri, uri_parms, body, logon_required,
             wait_for_completion):
        '''Operation: Set Auto-start List.'''
        # Extract CPC object-id from URI
        cpc_oid = uri_parms[0]
        
        # Get the CPC object
        cpc = hmc.cpcs.lookup_by_oid(cpc_oid)
        
        # Validate that the CPC is in a valid state for this operation
        if cpc.properties.get('status') not in ['active', 'service-required']:
            raise BadRequestError(
                method, uri, 
                "CPC is not in a valid state for setting auto-start list")
        
        # Extract auto-start list from request body
        auto_start_list = body.get('auto-start-list', [])
        
        # Validate auto-start list entries
        for entry in auto_start_list:
            if 'partition-uri' not in entry:
                raise BadRequestError(
                    method, uri,
                    "Auto-start list entry missing required 'partition-uri' field")
            
            partition_uri = entry['partition-uri']
            try:
                # Validate that the partition exists and belongs to this CPC
                partition_oid = partition_uri.split('/')[-1]
                partition = cpc.partitions.lookup_by_oid(partition_oid)
            except KeyError:
                raise BadRequestError(
                    method, uri,
                    f"Partition with URI '{partition_uri}' not found")
        
        # Update the CPC's auto-start list
        cpc.properties['auto-start-list'] = auto_start_list
        
        # Return success response
        return {}