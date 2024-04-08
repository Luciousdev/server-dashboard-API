from src.init import StartServer

server = StartServer()
server.init_routes()

if __name__ == "__main__":
    server.app.run(port=5001, debug=True)