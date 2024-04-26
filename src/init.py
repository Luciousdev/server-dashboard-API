from flask import Flask
from flask import jsonify, request
from src.components.uptime_kuma.index import get_all_monitors
from src.components.tn_scale.index import main
from src.components.ping.index import init as ping_init


class StartServer:
    def set_global_variables(self) -> None:
        global base_url
        base_url = "/api/"

    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.set_global_variables()

    def init_routes(self) -> None:
        @self.app.route(base_url+"/ping", methods=["GET"])
        def ping():
            return "pong"

        @self.app.route(base_url+"kuma-get-all-monitors", methods=["GET"])
        async def kuma():
            try:
                kuma_api = await get_all_monitors()
                response = jsonify(kuma_api)
                response.status_code = 203
                return response
            except Exception as e:
                response = jsonify({"status": 500, "error": f"An error occurred while connecting to Uptime Kuma: {e}"})
                response.status_code = 500
                return response

        @self.app.route(base_url+"tn-get-data", methods=["GET"])
        async def tn():
            try:
                data = await main(request.args.get("type"))
                response = jsonify({"status": 200, "data": data})
                return response
            except Exception as e:
                response = jsonify({"status": 500, "error": f"An error occurred while connecting to TrueNAS system: {e}"})
                response.status_code = 500
                return response

        @self.app.route(base_url+"ping-server", methods=["GET"])
        def ping_server():
            try:
                address = request.args.get("address")
                ptype = request.args.get("type")
                if not address:
                    return jsonify({"status": 400, "error": "Address is required"}), 400

                result = ping_init(address, ptype) if ptype else ping_init(address)
                return jsonify({"status": 200, "message": "Ping request sent", "data": result}), 200
            except Exception as e:
                response = jsonify({"status": 500, "error": f"An error occurred while sending ping request: {e}"})
                response.status_code = 500
                return response
