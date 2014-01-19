import codecs
import feedparser
import re
import unicodedata

# Stolen from django
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    re.sub('[-\s]+', '-', value)
    return value


d = feedparser.parse('input.xml')

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
  filename = '_posts/%s-%s-%s-%s.md' % (date.tm_year, date.tm_mon, date.tm_mday, title)
  f = codecs.open(filename, 'w', 'utf-8')
  f.write(post.content[0].value)
  f.close()

