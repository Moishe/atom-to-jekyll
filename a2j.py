import argparse
import codecs
import feedparser
import html2text
import os
import re
import sys
import unicodedata

# Stolen from django
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = re.sub('[-\s]+', '-', value)
    value = re.sub(' ', '_', value)
    return value

def getmarkdown(s):
    # disable line-wrapping on html2text output
    h = html2text.HTML2Text()
    h.body_width = 0
    h.escape_snob = 1
    return h.handle(s)

parser = argparse.ArgumentParser(description="Convert feed file (from eg. Blogger Takeout) to Jekyll _posts directory")
parser.add_argument('--source', '-s', type=argparse.FileType('r'), nargs='?', default=sys.stdin,
                    help='The source atom file.')
parser.add_argument('--dest', '-d', required=True,
                    help='The path to the _posts directory for output, eg. ~/src/foo.github.io/_posts')
parser.add_argument('--create-dir', '-c', action='store_true', default=False,
                    help='If true, and the output directory doesn\'t exist, create it. Will not delete existing directory.')
parser.add_argument('--force-overwrite', '-f', action='store_true', default=False,
                    help='If true, overwrite existing files. If false, skip existing files.')

args = parser.parse_args()

if not os.path.exists(args.dest):
    if args.create_dir:
        os.mkdir(args.dest)
    else:
        sys.stderr.write("ERROR: Destination path (%s) does not exist. Use --create-dir to force create.\n" % args.dest)
        sys.exit(1)

d = feedparser.parse(args.source)

posts = []

for entry in d.entries:
    try:
        if (entry.tags[0].term == u'http://schemas.google.com/blogger/2008/kind#post' and
            not hasattr(entry, 'app_draft') or entry.app_draft != u'yes'):
            posts.append(entry)
    except AttributeError:
        pass

print 'Converting %s posts.' % len(posts)

for post in posts:
    date = post.published_parsed
    if post.title:
        title = slugify(post.title)
    else:
        title = 'untitled'

    filename = '%s/%s-%s-%s-%s.md' % (args.dest, date.tm_year, date.tm_mon, date.tm_mday, title)
    if os.path.exists(filename):
        if args.force_overwrite:
            print "overwriting %s" % filename
        else:
            print "skipping existing file %s" % filename
            continue
    else:
        print "creating %s" % filename

    front_matter = '\n'.join((
                '---',
                'layout: post',
                'title: %s' % getmarkdown(title),
                '---\n'))
    f = codecs.open(filename, 'w', 'utf-8')
    f.write(front_matter)

    f.write(getmarkdown(post.content[0].value))
    f.close()
