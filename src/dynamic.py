#!/usr/bin/python

W = 20
#weight,value pairs.
items = [(i,i*2) for i in range(1,21)]

def get_profit(m,i,w,indent=0):
	'''i, index into items. w, max weight bound.'''
	print " "*indent + "Getting profit for" + str( (i,w))
	if i <= 0:
		#terminate recursion
		print " "*indent + "i was <= 0. returning 0"
		return 0
	if (i,w) in m:
		#already have answer
		print " "*indent + "Already had an answer. returning " + str(m[(i,w)])
		return m[(i,w)]
	w_i = items[i][0]
	v_i = items[i][1]
	if w_i > w:
		#if this item alone would go overweight.
		m[(i,w)] = get_profit(m,i-1,w,indent+1)
		print " "*indent + "This item alone would go overweight. Returning " + str(m[(i,w)])
		return m[(i,w)]
	m[(i,w)] = max(get_profit(m,i-1,w,indent+1), get_profit(m,i-1,w-w_i,indent+1)+v_i)
	print " "*indent + "Finally returning " + str(m[(i,w)])
	return m[(i,w)]
	

def main():
	n = len(items)-1
	m = {}
	print "Capacity: %d" % W
	print "Items: %s" % str(items)
	print get_profit(m,n,W)

if __name__ == "__main__":
	main()
