import random
import math

def nd(x): return math.e**(-(3*x)**2)

def wtrand(func):
  x = random.random()
  y = random.random()
  if (y<func(x)):
    return x
  else:
    return wtrand(func)

def delinb(l,p,ep):
  nu = l.replace(p,"@").replace(ep,"@").split("@")
  l = "".join([nu[j] for j in range(0,len(nu),2)])  
  return l

def sentcase(s):
	for p in ["?",".","!",";"]:
		for c in "abcdefghijklmnopqrstuvwxyz":
			s = s.replace(p+" "+c,p+" "+c.upper())
			s = s.replace("\n"+c,"\n"+c.upper())
			s = s.replace(" i "," I ")
	return s[0].upper() + s[1:]
