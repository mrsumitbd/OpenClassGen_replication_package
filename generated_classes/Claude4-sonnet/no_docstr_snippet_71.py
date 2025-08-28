class WebAppClient:

    @classmethod
    def create(cls, cmd, name, resource_group_name, webapp_json):
        from azure.cli.command_modules.appservice.custom import create_webapp
        from azure.cli.core.commands import LongRunningOperation
        
        poller = create_webapp(cmd, resource_group_name, name, webapp_json.get('plan'), 
                              webapp_json.get('runtime'), webapp_json.get('startup_file'),
                              webapp_json.get('deployment_container_image_name'),
                              webapp_json.get('deployment_source_url'),
                              webapp_json.get('deployment_source_branch'),
                              webapp_json.get('deployment_local_git'),
                              webapp_json.get('docker_registry_server_password'),
                              webapp_json.get('docker_registry_server_user'),
                              webapp_json.get('multicontainer_config_type'),
                              webapp_json.get('multicontainer_config_file'),
                              webapp_json.get('tags'),
                              webapp_json.get('using_webapp_up'))
        
        return LongRunningOperation(cmd.cli_ctx)(poller)

    @classmethod
    def restart(cls, cmd, resource_group_name, name, slot=None):
        from azure.cli.command_modules.appservice.custom import restart_webapp
        
        return restart_webapp(cmd, resource_group_name, name, slot)