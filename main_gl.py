import sys
import unittest

from jfa.jfaapp import JfaApp
from fw.fw import Fw, FwPyGame

from jfa.jfastepstest import TestJfaSteps

# pip install PyOpenGL
# jfa paper https://www.comp.nus.edu.sg/~tants/jfa/i3d06.pdf
# TODO uniform "tint" for programBlit

def main():
    """
    The main function initializes the game window, creates an instance of the application,
    and starts the game loop.
    """

    windowSize = 800, 600

    # Initialize the game framework with the specified window size
    fw = Fw(windowSize)

    # Create an instance of the application using the initialized framework
    app = JfaApp(fw)

    # Start the game loop using the framework and the application instance
    FwPyGame.gameLoop(fw, app)

    fw.release()

if __name__ == "__main__":    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main()
    else:
        main()
    