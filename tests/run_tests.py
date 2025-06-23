import subprocess
import sys
import os

def run_tests():
    """Run the test suite with pytest."""
    print("🧪 Running AI Chatbot Tests...")
    print("=" * 50)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    cmd = [
        sys.executable, "-m", "pytest",
        "test_main.py",
        "-v",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\nAll tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\nTests failed with exit code {e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print("pytest not found. Please install it with: pip install pytest")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())