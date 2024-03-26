# Adaugati toate testele pe care le-ati implementat in framework-ul unit test intr-o suita de teste
# Rulati testele direct din suita de teste
# Generati raportul de executie si interpretati-l

import unittest

import HtmlTestRunner

from Sesiunea_11.tema_s11 import MyTestCase


class TestElefantSuite(unittest.TestCase):

    def test_suite(self):
        test_suite = unittest.TestSuite()
        test_suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(MyTestCase)
        ])

        runner = HtmlTestRunner.HTMLTestRunner(
            combine_reports=True,
            report_title="Elefant Tests Report",
            report_name="Test Results"
        )

        runner.run(test_suite)
