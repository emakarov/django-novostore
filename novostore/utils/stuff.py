import random
import string
from django.http import QueryDict

def codegenerator(x,y,z):
  digits = "".join( [random.choice(string.digits) for i in xrange(x)] )
  chars = "".join( [random.choice(string.letters) for i in xrange(y)] ).lower()
  digits2 = "".join( [random.choice(string.digits) for i in xrange(z)] )
  return digits+chars+digits2

def deserialize_form(data):
    """
    Create a new QueryDict from a serialized form.
    """
    return QueryDict(query_string=unicode(data).encode('utf-8'))