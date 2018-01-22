try:
    from exceptions import AssertionError
except ImportError:
    pass
import logging
import sys
import time
import unittest

import stomp
from stomp.listener import TestListener
from stomp.test.testutils import *

log = logging.getLogger('ss_test.py')


class TestWithStompServer(unittest.TestCase):

    def test_disconnect(self):
        server = TestStompServer('127.0.0.1', 60000)
        try:
            server.start()

            server.add_frame('''CONNECTED
version: 1.1
session: 1
server: test
heart-beat: 1000,1000\x00''')

            conn = stomp.Connection([('127.0.0.1', 60000)])
            listener = TestListener()
            conn.set_listener('', listener)
            conn.start()
            conn.connect()

            time.sleep(2)

            server.stop()

            for _ in range(100):
                if server.stopped:
                    break
                time.sleep(0.1)
            else:
                assert False, 'server never disconnected'

            time.sleep(1)

            try:
                conn.send(body='test disconnect', destination='/test/disconnectqueue')
                self.fail('Should not have successfully sent a message at this point')
            except Exception:
                _, e, _ = sys.exc_info()
                if e.__class__ == AssertionError:
                    self.fail(str(e))
                log.debug('stopping conn after expected exception %s' % e)
                # lost connection, now restart the server
                try:
                    conn.disconnect(receipt=None)
                except:
                    pass

                time.sleep(2)

                server.add_frame('''CONNECTED
version: 1.1
session: 1
server: test
heart-beat: 1000,1000\x00''')

                server.start()

                conn.start()
                conn.connect()

                time.sleep(5)

            self.assertTrue(listener.connections >= 2, 'should have received 2 connection acknowledgements')

            time.sleep(2)
        finally:
            server.stop()
