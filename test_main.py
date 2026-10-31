import unittest

from main import PROJECT, get_status


class TestAetherCog(unittest.TestCase):

    def test_project_identity(self):
        self.assertEqual(PROJECT["short_name"], "AetherCog")
        self.assertEqual(PROJECT["version"], "0.1.0")

    def test_architecture_has_three_layers(self):
        self.assertEqual(
            PROJECT["architecture"],
            [
                "Cognitive Layer",
                "Simulation Layer",
                "Execution Layer",
            ],
        )

    def test_status_structure(self):
        status = get_status()

        self.assertEqual(status["project"], "AetherCog")
        self.assertEqual(status["version"], "0.1.0")
        self.assertEqual(status["status"], "operational")
        self.assertIn("python_version", status)
        self.assertEqual(len(status["architecture"]), 3)


if __name__ == "__main__":
    unittest.main()
