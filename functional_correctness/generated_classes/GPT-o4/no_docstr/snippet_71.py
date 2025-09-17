class WebAppClient:

    @classmethod
    def create(cls, cmd, name, resource_group_name, webapp_json):
        client = get_mgmt_service_client(cmd.cli_ctx, WebSiteManagementClient)
        site_envelope = Site(**webapp_json)
        return client.web_apps.create_or_update(resource_group_name, name, site_envelope)

    @classmethod
    def restart(cls, cmd, resource_group_name, name, slot=None):
        client = get_mgmt_service_client(cmd.cli_ctx, WebSiteManagementClient)
        if slot:
            return client.web_apps.restart_slot(resource_group_name, name, slot)
        return client.web_apps.restart(resource_group_name, name)