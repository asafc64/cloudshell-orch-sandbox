from cloudshell.api.cloudshell_api import AppInfo

from cloudshell.workflow.orchestration.app import App


class Components(object):
    def __init__(self, resources, services, apps):
        self.resources = dict((resource.Name, resource) for resource in resources)
        """:type : dict[str, ReservedResourceInfo]"""
        self.services = dict((service.Alias, service) for service in services)
        """:type : dict[str, ServiceInstance]"""
        self.apps = dict((app.Name, App(app)) for app in apps if len(app.DeploymentPaths) > 0)  # avoid bug in
        # cloudshell-automation-api where an app named None returns even when there are no apps in the reservation
        """:type : dict[str, App]"""

    def get_apps_by_name_contains(self, name):
        """
        :param str name:
        :return:
        """
        return [value for key, value in self.apps.iteritems() if name in key]

    def get_resources_by_model(self, model):
        """
        :param str model:
        :return:
        """
        return [value for key, value in self.resources.iteritems() if model == value.ResourceModelName]

    def get_services_by_alias(self, alias):
        """
        :param str alias:
        :return:
        """
        return [value for key, value in self.services.iteritems() if alias == value.Alias]

    def get_services_by_name(self, name):
        """
        :param str name:
        :return:
        """
        return [value for key, value in self.services.iteritems() if name == value.ServiceName]

    def update_deployed_apps_information_after_bulk_deployment(self, sandbox, deployment_results):
        """
        :param Sandbox sandbox: 
        :param DeployAppToCloudProviderBulkInfo deployment_results:
        :return:
        """
        reservation_resources = sandbox.automation_api.GetReservationDetails(
            sandbox.id).ReservationDescription.Resources

        self.resources = dict((resource.Name, resource) for resource in reservation_resources)

        for resource_name, resource in self.resources.iteritems():
            if isinstance(resource.AppDetails, AppInfo):  # if deployed app
                if resource.AppDetails.AppName in self.apps:
                    self.apps[resource.AppDetails.AppName].set_deployed_app_resource(resource)
