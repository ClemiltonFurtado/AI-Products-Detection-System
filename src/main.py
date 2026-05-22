"""
Main entry point for the AI Products Detection System.

This script is responsible for starting the application. It instantiates the 
central system orchestrator (Wutils), which in turn loads the Artificial 
Intelligence model, configures the API routes, and starts the Flask server.
"""

from Wutils.wutils import Wutils

def main():
    """
    Main execution function.
    Initializes the system utilities and triggers the web server execution.
    """
    wutils = Wutils()
    
    wutils.initialize_system()


if __name__ == '__main__':
    main()