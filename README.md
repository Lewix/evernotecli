# Evernote CLI

A simple command-line interface for Evernote. It supports listing, creating and updating notes in various notebooks.

    Usage:
        note ls [<notebook>]
        note notebooks
        note print [<title>] [--notebook=<notebook_name>]
        note [<title>] [--notebook=<notebook_name>]

`note` and `note print` both support input from stdin, so it's possible to chain commands like so:

    note ls | grep something | note

To edit existing notes with "something" in their title.

# Configuration

Configuration is done in the `evernote.cfg` file. See `evernotecli.cfg.sample` for an example configuration file. You will need a developer token from Evernote.
