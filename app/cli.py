import os
import click


def register(app):
    @app.cli.group()
    def test_cmd():
        """Just a test command"""
        pass
