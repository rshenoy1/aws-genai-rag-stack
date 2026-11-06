
import unittest
import squad

class TestMultiAgentSquad(unittest.TestCase):

    def test_web_search_tool_data_integrity(self):
        """Validates that the web search tool accurately extracts facts"""
        tool_output = squad.tool_web_search("copper shortage")
        self.assertIn("copper shortage", tool_output)
        self.assertTrue(tool_output.startswith("CURRENT FACT:"))

    def test_secure_calculator_tool_execution(self):
        """Validates math tool parsing for specific business metrics"""
        math_output = squad.tool_secure_calculator("100 * 1.15 overhead")
        self.assertEqual(math_output, "115.00")

    def test_writer_agent_report_synthesis(self):
        """Ensures the Writer Agent correctly merges contextual data inputs"""
        mock_research = "Fact: Copper Spiked"
        mock_analysis = "Report: Total Cost $115.00"
        
        compiled_report = squad.worker_writer(mock_research, mock_analysis)
        
        self.assertIn("=== EXECUTIVE COMPLIANCE REPORT ===", compiled_report)
        self.assertIn(mock_research, compiled_report)
        self.assertIn(mock_analysis, compiled_report)

if __name__ == "__main__":
    unittest.main()

