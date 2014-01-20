A simple script to convert an atom file produced by Blogger export to a set of files in a _post directory, for use by Jekyll.

Requires:

 - [html2text](https://github.com/Moishe/html2text) with patch to not add line breaks inside spans.
 - [feedparser](https://pypi.python.org/pypi/feedparser)

Install the above two packages first.

Run 'python a2j.py -h' for a list of command-line arguments.