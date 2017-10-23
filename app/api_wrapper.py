
import requests
import json


class TransportAPIWrapper:
    """
    Wrapper for Lviv public transport API.
    """

    BASE_URL = 'http://82.207.107.126:13541/SimpleRide/LAD/SM.WebApi/api'
    ALL_ROUTES = BASE_URL + '/CompositeRoute'
    ROUTE_PATH = BASE_URL + '/path/?code=LAD|'
    ROUTE_MONITORING = BASE_URL + '/RouteMonitoring/?code=LAD|'
    ALL_STOPS = BASE_URL + '/stops'
    ROUTE_STOPS = BASE_URL + '/CompositeRoute/?code=LAD|'
    STOP_INFO = ALL_STOPS + '/?code='

    ROUTES = dict()

    # pay attention:
    # route: ?code=<id>
    # stop: ?code=<code> 

    def __init__(self):
        self._get_routes()

    # @classmethod
    def _get_routes(self):
        """
        Method to fetch all routes and all related info (route path,
        route stops) and store in class variable ROUTES.
        """
        all_routes_resp = requests.get(self.ALL_ROUTES)

        for route in json.loads(all_routes_resp.json()):
            self.ROUTES.update(
                {route.get('Id'): {'id': route.get('Id'),
                                   'name': route.get('Name'),
                                   'code': route.get('Code')}})

    def _update_routes(self):
        """
        Method to update class variable ROUTES.
        """
        pass

    def routes(self):
        """
        Method to get all available routes.
        """
        response = requests.get(self.ALL_ROUTES)
        return json.loads(response.json())

    def stops(self):
        """
        Method to get all available stops.
        """
        response = requests.get(self.ALL_STOPS)
        # TODO: change keys name s to camel_case
        return json.loads(response.json())

    def route_monitoring(self, route_id):
        """
        Method to get all vehicles on route.
        """
        response = requests.get("{}{}".format(self.ROUTE_MONITORING, route_id))
        return json.loads(response.json())

    def route_stops(self, route_id):
        """
        Method to get all stops on route.
        """
        response = requests.get("{}{}".format(self.ROUTE_STOPS, route_id))
        return json.loads(response.json())

    def route_path(self, route_id):
        """
        Method to get coordinates of route's path to draw it on map.
        """
        response = requests.get("{}{}".format(self.ROUTE_PATH, route_id))
        return json.loads(response.json())

    def info(self, stop_id):
        """
        Method to get info about all vehicles that arrive on stop.
        """
        response = requests.get("{}{}".format(self.STOP_INFO, stop_id))
        return json.loads(response.json())


print()