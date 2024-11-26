# tests/test_main.py
import subprocess

def test_startup_message(capsys):
    """
    Test that the program prints the correct startup message.
    """
    # Run the main.py script
    subprocess.run(["python3", "src/main.py"], check=True)

    # Capture printed output
    captured = capsys.readouterr()
    assert "-- Starting PortfolioManager --" in captured.out
