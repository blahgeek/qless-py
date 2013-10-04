'''A worker that serially pops and complete jobs'''

import time
import threading
from qless import logger

from . import Worker


class SerialWorker(Worker):
    '''A worker that just does serial work'''
    def signals(self):
        '''Register all of our signal handlers'''
        # QUIT - Wait for child to finish processing then exit
        # TERM / INT - Immediately kill child then exit
        # USR1 - Immediately kill child but don't exit
        # USR2 - Don't start to process any new jobs
        # CONT - Start to process new jobs again after a USR2
        pass

    def kill(self, jid):
        '''The best way to do this is to fall on our sword'''
        if jid in self.jids:  # pragma: no cover
            exit(1)

    def run(self):
        '''Run jobs, popping one after another'''
        self.reconnect()
        # Register our signal handlers
        self.signals()

        # # First things first, we should clear out any jobs that
        # # we're responsible for off-hand
        # while len(self.jids):
        #     try:
        #         job = self.client.jobs[self.jids.pop(0)]
        #         # If we still have access to it, then we should process it
        #         if job.heartbeat():
        #             logger.info('Resuming %s' % job.jid)
        #             self.title('Working %s (%s)' % (job.jid, job.klass_name))
        #             job.process()
        #         else:
        #             logger.warn(
        #                 'Lost heart on would-be resumed job %s' % job.jid)
        #     except KeyboardInterrupt:
        #         return
        thread = threading.Thread(target=self.listen)
        try:
            thread.start()
            for job in self.jobs():
                # If there was no job to be had, we should sleep a little bit
                if not job:
                    self.title('Sleeping...')
                    logger.debug('Sleeping for %fs' % self.interval)
                    time.sleep(self.interval)
                else:
                    self.title('Working on %s (%s)' % (job.jid, job.klass_name))
                    job.process()
        finally:
            thread.join()