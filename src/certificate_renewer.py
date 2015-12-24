from threading import Thread
import logging

class CertificateRenewer(Thread):
    def __init__(self, renew_queue, error_queue):
        super(CertificateRenewer, self).__init__()
        self.renew_queue = renew_queue
        self.error_queue = error_queue

    def run(self):
        while True:
            logging.debug('[certificate-renewer] Watching for certificate')
            certificate = self.renew_queue.get()
            logging.info('[certificate-renewer][%s] Renewing' % certificate.name)
            certificate.renewed()
