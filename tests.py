import unittest

from heavyeggs.models import File
from heavyeggs import create_app

class FileTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        
        self.ctx = self.app.test_request_context()
        print self.app.url_map

        with self.ctx:
            self.file = File.query.get(6)

    def test_paths(self):
        with self.ctx:
            self.file.get_thumbnail_url()

if __name__ == '__main__':
    unittest.main()
