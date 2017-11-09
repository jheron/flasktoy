from app import app
import unittest 
import httplib, urllib

class FlaskBookshelfTests(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    def tearDown(self):
        pass 

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 200) 

    def test_health_check(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/health') 

        # assert the response data
        self.assertEqual(result.data, "0")

    def test_functional_200(self):
        conn = httplib.HTTPConnection("localhost")
        conn.request("GET", "/health")
        resp = conn.getresponse()
        self.assertEqual(resp.status, 200)

    def test_functional_reason(self):
        conn = httplib.HTTPConnection("localhost")
        conn.request("GET", "/health")
        resp = conn.getresponse()
        self.assertEqual(resp.reason, "OK")

    def test_functional_smoke(self):
        conn = httplib.HTTPConnection("localhost")
        conn.request("GET", "/health")
        resp = conn.getresponse()
        self.assertEqual(resp.read(), "1")

# runs the unit tests in the module
if __name__ == '__main__':
      unittest.main()
