
import unittest
from unittest.mock import patch
import ingest
import query

class TestGenAIPipeline(unittest.TestCase):

    def test_lambda_s3_ingestion_payload(self):
        mock_s3_event = {
            "Records": [{
                "s3": {
                    "bucket": {"name": "test-data-lake"},
                    "object": {"key": "handbook.txt"}
                }
            }]
        }
        with patch("ingest.ENV_MODE", "LOCAL"):
            try:
                ingest.lambda_handler(mock_s3_event, None)
                success = True
            except Exception:
                success = False
            self.assertTrue(success)

    def test_api_gateway_query_routing(self):
        with patch("query.ENV_MODE", "LOCAL"):
            response = query.run_query("How many weeks of paternity leave do I get?")
            self.assertIn("12 weeks", response)

if __name__ == "__main__":
    unittest.main()

