import threading
import flask
import os

class DownloadListener:

    app = flask.Flask(__name__)

    @app.route('/file/<file_id>', methods=['GET'])
    def download(file_id):
        file_path = f'../audio/{file_id}'
        try:
            return flask.send_file(file_path, as_attachment=True)
        except FileNotFoundError:
            return flask.abort(404)


    def __init__(self, host_ip: str, port: int):
        self.host_ip = host_ip
        self.port = port

    def generate_download_link(self, file_path):
        file_id = file_path.split("/")[-1]
        return f'http://{self.host_ip}:{self.port}/file/{file_id}'

    def run(self):
        self.app.run(port=self.port, host="0.0.0.0", debug=False)

    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()