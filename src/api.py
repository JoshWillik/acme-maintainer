from flask import Flask, request
import json
import certificate

def render_json(func):
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        if type(res) is not tuple:
            res = (res, 200)

        data = json.dumps(res[0])
        status = res[1]
        try:
            headers = res[2]
        except:
            headers = {}
        headers.update({
            'Content-Type': 'application/json'
        })
        return (data, status,headers)
    return inner

def create(db):
    manager = certificate.CertificateManager(db)
    app = Flask(__name__)

    @app.route('/certificates', methods=['GET'])
    @render_json
    def find_all_certificates():
        return [cert.get_all() for cert in manager.find_all()]

    @app.route('/certificates', methods=['POST'])
    def create_certificate():
        cert = manager.create(request.json)
        try:
            cert.save()
            return (json.dumps({'certificate': cert.get_all()}), 201)
        except Exception as e:
            print(e)
            return (json.dumps({'error': 'could_not_save'}), 500,)

    return app
