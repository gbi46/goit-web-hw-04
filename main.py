from servers import run_http_server, run_socket_server
from threading import Thread

def boot_socket_server(name):
    socket_server = Thread(name=name, target=run_socket_server)
    socket_server.start()

    return socket_server

def boot_http_server(name):
    http_server = Thread(name=name, target=run_http_server)
    http_server.start()

    return http_server

def run():
    servers = {
        "HTTP_SERVER": boot_http_server,
        "SOCKER_SERVER": boot_socket_server
    }

    threads = {}
   
    for name, server in servers.items():
        thread = server(name)
        threads[thread.name] = thread

    for name, th in threads.items():
        if not th.is_alive():
            print("thread is not alive") 
            thread = servers[name](name)
            threads[name] = thread

if __name__ == "__main__":
    run()
