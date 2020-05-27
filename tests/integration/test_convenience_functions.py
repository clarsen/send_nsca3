from .nsca_test_case import NSCATestCase, ServiceCheckResult

import send_nsca3


class ConvenienceFunctionTest(NSCATestCase):
    crypto_method = 3

    def assertions(self, status, message):
        checks = self.expect_checks(1)
        self.assertEqual(len(checks), 1)
        self.assertEqual(checks[0], ServiceCheckResult(host_name='myhost', service_name='myservice', status=status, output=message))

    def test_send_nsca(self):
        send_nsca3.send_nsca(0, b'myhost', b'myservice', b'test_send_nsca', **self.nsca_sender_args)
        self.assertions(0, 'test_send_nsca')

    def test_nsca_ok(self):
        send_nsca3.nsca_ok(b'myhost', b'myservice', b'test_nsca_ok', **self.nsca_sender_args)
        self.assertions(0, 'test_nsca_ok')

    def test_nsca_warning(self):
        send_nsca3.nsca_warning(b'myhost', b'myservice', b'test_nsca_warning', **self.nsca_sender_args)
        self.assertions(1, 'test_nsca_warning')

    def test_nsca_critical(self):
        send_nsca3.nsca_critical(b'myhost', b'myservice', b'test_nsca_critical', **self.nsca_sender_args)
        self.assertions(2, 'test_nsca_critical')

    def test_nsca_unknown(self):
        send_nsca3.nsca_unknown(b'myhost', b'myservice', b'test_nsca_unknown', **self.nsca_sender_args)
        self.assertions(3, 'test_nsca_unknown')
