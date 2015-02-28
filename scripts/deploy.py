#!/usr/env/bin python

"""
Deployment script for the Mainlands 7 web site.

Transforms the site content as it exists in version control to the format
required on the web server.

It accepts the following positional command-line arguments:

[1] src - The path to the source directory.  This should be the wwwroot
    directory in the version control repository.

[2] dst - The path to the destination directory.  Upon completion of the
    script, the content of this directory may be uploaded as-is to the web
    server.
"""

import enum
import os
import shutil
import sys
import zipfile

class ExitCode(enum.IntEnum):
    success = 0
    failure = 1

class Main:
    def __init__(self):
        self._source_path = None
        self._destination_path = None

    @staticmethod
    def _add_directory_to_zip_file(zip_file, directory_path):
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                zip_file.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), directory_path))

    def _copy_content(self):
        shutil.copytree(self._source_path, self._destination_path)

    def _create_archive_from_directory(self, directory_path_relative_to_destination_path):
        directory_path = os.path.join(self._destination_path, directory_path_relative_to_destination_path)
        zip_file_path = directory_path + '.zip'
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            Main._add_directory_to_zip_file(zip_file, directory_path)
        shutil.rmtree(directory_path)

    def _create_archives(self):
        self._create_archive_from_directory(os.path.join('htdocs', 'documents', 'liaison', 'records-inspection-2013-12-03'))
        self._create_archive_from_directory(os.path.join('htdocs', 'documents', 'liaison', 'records-inspection-2013-12-03-raw'))

    def _parse_args(self):
        if len(sys.argv) != 3:
            return False

        self._source_path = sys.argv[1]
        self._destination_path = sys.argv[2]
        return True

    def _print_usage(self):
        print('usage: deploy.py <src> <dst>')

    def main(self):
        if not self._parse_args():
            self._print_usage()
            return ExitCode.failure
        
        self._copy_content()
        self._create_archives()
        return ExitCode.success

if __name__ == '__main__':
    sys.exit(Main().main())
