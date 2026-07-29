import sys
import os
import unittest

# Ensure project root is in sys.path so we can import from modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.analyzer import parse_recon_output, analyze_findings


class TestAnalyzerParsing(unittest.TestCase):

    def test_valid_json_parsing(self):
        """Tests parsing of valid JSON output from Go engine."""
        sample_json = '[{"port": 80, "banner": "Apache"}, {"port": 22, "banner": "OpenSSH"}]'
        result = parse_recon_output(sample_json)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["port"], 80)

    def test_empty_output_parsing(self):
        """Tests handling of empty string input."""
        result = parse_recon_output("")
        self.assertIsNone(result)

    def test_invalid_json_parsing(self):
        """Tests graceful failure on malformed JSON string."""
        invalid_json = '{"port": 80, "banner": "Apache"'  # Unclosed string
        result = parse_recon_output(invalid_json)
        self.assertIsNone(result)

    def test_non_list_json_parsing(self):
        """Tests rejection of valid JSON that is not a list structure."""
        dict_json = '{"port": 80, "status": "open"}'
        result = parse_recon_output(dict_json)
        self.assertIsNone(result)


class TestAnalyzerRiskEngine(unittest.TestCase):

    def test_risk_score_calculation(self):
        """Tests threat score calculation and risk mapping for known ports."""
        sample_parsed_data = [
            {"port": 23, "banner": "Telnet prompt"},  # Telnet -> CRITICAL (10)
            {"port": 22, "banner": "OpenSSH"}         # SSH -> LOW (1)
        ]
        analysis = analyze_findings(sample_parsed_data)
        
        self.assertEqual(analysis["total_open_ports"], 2)
        self.assertEqual(analysis["overall_threat_score"], 11)  # 10 + 1 = 11
        self.assertEqual(analysis["findings"][0]["risk"], "CRITICAL")
        self.assertEqual(analysis["findings"][1]["risk"], "LOW")

    def test_unknown_port_handling(self):
        """Tests fallback logic for unmapped or custom ports."""
        sample_parsed_data = [
            {"port": 9999, "banner": "Custom App"}  # Unmapped port -> INFO (0)
        ]
        analysis = analyze_findings(sample_parsed_data)
        
        self.assertEqual(analysis["overall_threat_score"], 0)
        self.assertEqual(analysis["findings"][0]["risk"], "INFO")
        self.assertEqual(analysis["findings"][0]["service"], "Unknown")


if __name__ == "__main__":
    unittest.main()
