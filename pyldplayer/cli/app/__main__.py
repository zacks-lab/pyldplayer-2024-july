
if __name__ == "__main__":
    import os
    import sys
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    sys.path.insert(0, path)
    from pyldplayer.cli.app import app
    app()