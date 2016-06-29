import os
import unittest
from StringIO import StringIO

from smartfile import BasicClient
from smartfile.errors import ResponseError

API_KEY = os.environ.get("API_KEY")
API_PASSWORD = os.environ.get("API_PASSWORD")
TESTFN = "testfn"

if API_KEY is None:
    raise RuntimeError("API_KEY is required")

if API_PASSWORD is None:
    raise RuntimeError("API_PASSWORD is required")


class CustomOperationsTestCase(unittest.TestCase):

    def setUp(self):
        self.api = BasicClient(API_KEY, API_PASSWORD)
        # Make directory for tests
        self.api.post('/path/oper/mkdir/', path='/testfn2')

    def get_data(self):
        data = self.api.get("/path/info/testfn")
        return data

    def tearDown(self):
        self.api.remove('/testfn2')
        os.remove('testfn')

    def upload(self):
        file_contents = "hello"
        f = StringIO(file_contents)
        f.seek(0)
        self.api.upload(TESTFN, f)
        self.assertEquals(self.get_data()['size'], f.len)

    def download(self):
        self.api.download('testfn')
        self.assertEquals(self.get_data()['size'], os.path.getsize('testfn'))

    def move(self):
        self.api.move('testfn', '/testfn2/')

    def remove(self):
        self.api.remove("/testfn2/testfn")
        with self.assertRaises(ResponseError):
            self.api.remove("/testfn2/testfn")

    def test_upload_download_move_delete(self):
        self.upload()
        self.download()
        self.move()
        self.remove()
