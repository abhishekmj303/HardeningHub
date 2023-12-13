import unittest
import subprocess
import sys

class TestScriptExecution(unittest.TestCase):
    # Assuming your main script is named 'main_script.py'
    script_path = 'BackEnd/readtoml.py'

    def test_run_commands(self):
        """Test if the script runs without errors."""
        try:
            # Execute the script
            result = subprocess.run(['python', self.script_path], check=True, capture_output=True)
        except subprocess.CalledProcessError as error:
            # This will automatically fail the test if an error occurs
            self.fail(f"Script execution failed: {error}")

if __name__ == "__main__":
    unittest.main()
