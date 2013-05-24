import random
import string

def codegenerator(x,y,z):
  digits = "".join( [random.choice(string.digits) for i in xrange(x)] )
  chars = "".join( [random.choice(string.letters) for i in xrange(y)] ).lower()
  digits2 = "".join( [random.choice(string.digits) for i in xrange(z)] )
  return digits+chars+digits2
