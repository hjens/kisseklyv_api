import unittest
from kisseklyv import hashid as ut

class TestUtilityFunctions(unittest.TestCase):
    def test_get_hashid_same_for_same_id(self):
        id = 1
        hash1 = ut.get_hashid_from_id(id)
        hash2 = ut.get_hashid_from_id(id)
        self.assertEqual(hash1, hash2)

    def test_get_hashid_different_for_different_id(self):
        id1 = 123
        id2 = 124
        hash1 = ut.get_hashid_from_id(id1)
        hash2 = ut.get_hashid_from_id(id2)
        self.assertNotEqual(hash1, hash2)

    def test_test_get_id_from_hashid(self):
        id = 123
        hashid = ut.get_hashid_from_id(id)
        id_back = ut.get_id_from_hashid(hashid)
        self.assertEqual(id_back, id)
