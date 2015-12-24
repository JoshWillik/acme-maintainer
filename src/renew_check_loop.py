from threading import Thread
from time import sleep
import settings
import logging
from datetime import datetime

class RenewCheckLoop(Thread):
    certificates = []
    renew_queue = None

    def __init__(self, renew_queue, warning_queue):
        super(RenewCheckLoop,self).__init__()
        self.renew_queue = renew_queue
        self.warning_queue = warning_queue

    def run(self):
        while True:
            now = datetime.now()
            logging.debug('[renew-check] Checking for certificates')
            for certificate in self.certificates:
                certificate.reload()
                last_update = certificate.last_renewed()
                logging.debug('[renew-check][%s] Last updated %s' % (certificate.name, last_update))
                if last_update is None or now - last_update >= settings.MAX_CERTIFICATE_AGE:
                    if not certificate.is_renewing():
                        logging.debug('[renew-check][%s] Renewing' % (certificate.name))
                        certificate.is_renewing(True)
                        self.renew_queue.put(certificate)
                    if last_update is not None and now - last_update > settings.CERTIFICATE_WARNING_AGE:
                        logging.warn('[renew-check][%s] Certificate is %i seconds old' % (now - last_update))
                        self.warning_queue.put(certificate)

            sleep(settings.RENEW_LOOP_SLEEP_SECONDS)

    def watch(self, certificate):
        self.certificates.append(certificate)
