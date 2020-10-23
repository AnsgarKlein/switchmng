import os
import unittest

from switchmng.schema import Base
from switchmng.schema import Connector
from switchmng.database import DatabaseConnection
from switchmng.config import *
from switchmng.importer import *

class Test_Importer(unittest.TestCase):
    """Test class that tests importer and example resources"""

    RESOURCE_FOLDER = 'examples'

    def setUp(self):
        self.db = DatabaseConnection('sqlite', '', False, Base)

    def test_import_fail1(self):
        """Import resources from directory that does not exist"""

        # Importing non existing path fails
        with self.assertRaises(ValueError):
            import_from_path(self.db, 'NON-EXISTING-PATH', None)

    def test_import_fail2(self):
        """Import resources from directory None"""

        # Importing path = None fails
        with self.assertRaises(ValueError):
            import_from_path(self.db, None, None)

    def test_import_recursive(self):
        """Import directory containing subdirectories with resources"""

        # Import
        import_from_path(self.db, self.RESOURCE_FOLDER, None)

        # Check all
        connectors = database.query_connectors(self.db.Session())
        self.assertTrue(len(connectors) > 0)

        protocols = database.query_network_protocols(self.db.Session())
        self.assertTrue(len(protocols) > 0)

        models = database.query_switch_models(self.db.Session())
        self.assertTrue(len(models) > 0)

    def test_import_named_dir(self):
        """Import resources from directory named like resource type"""

        top_dir = self.RESOURCE_FOLDER

        children = ( os.path.join(top_dir, child) for child in os.listdir(top_dir) )
        subdirs = [ child for child in children if os.path.isdir(child) ]
        subdirs = sort_import_dirs(subdirs)
        assert len(subdirs) > 0

        # Import resources from all subdirectories separately
        for subdir in subdirs:
            with self.subTest(subdir = subdir):
                import_from_path(self.db, subdir, None)

        # Check
        connectors = database.query_connectors(self.db.Session())
        self.assertTrue(len(connectors) > 0)

    def test_import_unnamed_dir(self):
        """Import resource directory with resource type explicitly stated"""

        top_dir = self.RESOURCE_FOLDER
        res_dir = os.path.join(top_dir, 'connectors')
        res_type = Connector

        # Import
        import_from_path(self.db, res_dir, res_type)

        # Check
        connectors = database.query_connectors(self.db.Session())
        self.assertTrue(len(connectors) > 0)

    def test_import_file(self):
        """Import resources from connectors directory separately"""

        top_dir = self.RESOURCE_FOLDER
        res_dir = os.path.join(top_dir, 'connectors')
        res_type = Connector

        children = [ os.path.join(res_dir, child) for child in os.listdir(res_dir) ]
        files = [ child for child in children if os.path.isfile(child) ]
        assert len(files) > 0

        # Only test a few files
        if len(files) > 3:
            files = files[:3]

        # Import resources from file separately
        for f in files:
            with self.subTest(f = f):
                import_from_path(self.db, f, res_type)

        # Import resources without specifying resource type fails
        for f in files:
            with self.subTest(f = f):
                with self.assertRaises(ValueError):
                    import_from_path(self.db, f, None)

        # Check
        connectors = database.query_connectors(self.db.Session())
        self.assertTrue(len(connectors) > 0)

if __name__ == '__main__':
    unittest.main(buffer = True)
