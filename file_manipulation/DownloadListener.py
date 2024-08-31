import threading
import flask

class DownloadListener:

    app = flask.Flask(__name__)

    @app.route('/file/<file_id>', methods=['POST'])
    def download(file_id):
        return flask.send_file('../audio/' + file_id)

    def __init__(self, host_ip: str, port: int):
        self.host_ip = host_ip
        self.port = port

    def generate_download_link(self, file_id):
        return f'http://{self.host_ip}:{self.port}/file/{file_id}'

    def run(self):
        self.app.run(port=self.port, debug=False)

    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
