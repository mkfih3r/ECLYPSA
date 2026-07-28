import unittest
from core.engine import EclypsaEngine

class TestEclypsaEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EclypsaEngine()

    def test_engine_initialization(self):
        self.assertTrue(self.engine.initialize())
        self.assertTrue(self.engine.is_running)

    def test_health_check(self):
        self.engine.initialize()
        health = self.engine.health_check()
        self.assertEqual(health["status"], "active")
        self.assertEqual(health["subsystems"]["core"], "healthy")

    def tearDown(self):
        self.engine.shutdown()

if __name__ == "__main__":
    unittest.main()