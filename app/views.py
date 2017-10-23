
from app import app, errors
from flask import render_template, jsonify, abort
from flask.views import MethodView
from .api_wrapper import TransportAPIWrapper

# Public transport API object
public_api = TransportAPIWrapper()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


class RoutesAPI(MethodView):
    """
    Class represents routes.
    """
    def get(self, route_id):
        """
        Get route info. Returns all routes or certain route by ID.
        For certain route returns info about stops and path.
        """
        if route_id:
            route = public_api.ROUTES.get(route_id, None)

            if not route:
                abort(404)

            route['path'] = public_api.route_path(route.get('id'))
            route['stops'] = public_api.route_stops(route.get('id'))

            return jsonify(route)

        else:
            routes = list(public_api.ROUTES.values())

            return jsonify(count=len(routes), routes=routes)


class StopsAPI(MethodView):
    """
    Get stops info
    """
    def get(self):
        stops = public_api.stops()

        # TODO: make each stop public i.e. monitoring url

        # for stop in stops:
        #     response.append(utils.make_public(stop, stop=True))
        return jsonify(count=len(stops), stops=stops)


class RouteInfoAPI(MethodView):
    """
    Get Route monitoring info i.e. each vehicle on route.
    """

    def get(self, route_id):
        vehicles = public_api.route_monitoring(route_id)
        return jsonify(vehicles_count=len(vehicles), vehicles_info=vehicles)


class StopInfoAPI(MethodView):
    """
    Get Stop monitoring info i.e. all vehicles that arrive on stop.
    """

    def get(self, stop_id):
        vehicles = public_api.info(stop_id)
        return jsonify(vehicles_count=len(vehicles), vehicles_info=vehicles)


# =====================   Register API endpoints   ==========================

routes_view = RoutesAPI.as_view('routes_api')

app.add_url_rule('/api/v1/routes/',
                 defaults={'route_id': None},
                 view_func=routes_view,
                 methods=['GET'])

app.add_url_rule('/api/v1/routes/<int:route_id>',
                 view_func=routes_view,
                 methods=['GET'])


stops_view = StopsAPI.as_view('stops_api')

app.add_url_rule('/api/v1/stops/',
                 view_func=stops_view,
                 methods=['GET'])


route_monitoring_view = RouteInfoAPI.as_view('route_monitoring')

app.add_url_rule('/api/v1/route_monitoring/<route_id>',
                 view_func=route_monitoring_view,
                 methods=['GET'])


stop_monitoring_view = StopInfoAPI.as_view('stop_monitoring')

app.add_url_rule('/api/v1/stop_monitoring/<stop_id>',
                 view_func=stop_monitoring_view,
                 methods=['GET'])
