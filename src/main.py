import database
import api
import settings
from renew_check_loop import RenewCheckLoop
from certificate_renewer import CertificateRenewer
from queue import Queue
import logging
import certificate

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    db = database.init()

    renew_queue = Queue()
    warning_queue = Queue()
    error_queue = Queue()
    checker = RenewCheckLoop(renew_queue, warning_queue)

    manager = certificate.CertificateManager(db)
    for certificate in manager.find_all():
        checker.watch(certificate)

    renewer = CertificateRenewer(renew_queue, error_queue)

    renewer.start()
    checker.start()

    api.create(db).run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
        use_reloader=False
    )
