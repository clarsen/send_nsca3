from .nsca_test_case import NSCATestCase, ServiceCheckResult, HostCheckResult


class TestBasicFunctionality(NSCATestCase):
    def test_service(self):
        nsca_sender = self.nsca_sender()
        nsca_sender.send_service(b'hello', b'goodbye', 1, b'test_service')
        checks = self.expect_checks(1)
        self.assertEqual(len(checks), 1)
        self.assertEqual(checks[0], ServiceCheckResult(host_name='hello', service_name='goodbye', status=1, output='test_service'))

    def test_host(self):
        nsca_sender = self.nsca_sender()
        nsca_sender.send_host(b'myhost', 3, b'test_host')
        checks = self.expect_checks(1)
        self.assertEqual(len(checks), 1)
        self.assertEqual(checks[0], HostCheckResult(host_name='myhost', status=3, output='test_host'))

    def test_both(self):
        import time
        # found some issue with the test, where it is taking 10+ seconds for the nsca process to receive
        # and write the submitted check to the nsca_fifo. (?). during this 10+ seconds, if we send a second
        # check, the first will never be written to nsca_fifo.
        nsca_sender = self.nsca_sender()
        nsca_sender.send_host(b'myhost', 3, b'test_both_host')
        time.sleep(15)
        nsca_sender.send_service(b'myhost', b'myservice', 0, b'test_both_service')
        checks = self.expect_checks(2)
        # ordering is unpredictable
        self.assertIn(HostCheckResult(host_name='myhost', status=3, output='test_both_host'), checks)
        self.assertIn(ServiceCheckResult(host_name='myhost', service_name='myservice', status=0, output='test_both_service'), checks)
