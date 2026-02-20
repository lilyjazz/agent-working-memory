import unittest
import sys
import os

def run_tests():
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    
    # Change to the tests directory
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(curr_dir)
    
    # 1. Run Unit Tests (Fast, Safe)
    print("========================================")
    print("🧪 Running UNIT Tests (Mocked)...")
    print("========================================")
    # top_level_dir=curr_dir ensures discovery logic stays within bounds
    suite = loader.discover('unit', pattern='test_*.py', top_level_dir=curr_dir)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        print("\n❌ Unit tests failed!")
        sys.exit(1)

    # 2. Run Integration Tests (Slow, Real Network)
    # Check env var to see if we should skip live tests
    if os.environ.get("SKIP_LIVE_TESTS"):
        print("\nSkipping Live Tests (SKIP_LIVE_TESTS is set).")
        return

    print("\n========================================")
    print("🌍 Running INTEGRATION Tests (Live Network)...")
    print("   Note: This will create real TiDB Zero databases.")
    print("========================================")
    suite_live = loader.discover('integration', pattern='test_*.py', top_level_dir=curr_dir)
    result_live = runner.run(suite_live)

    if not result_live.wasSuccessful():
        print("\n❌ Integration tests failed!")
        sys.exit(1)
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    run_tests()
