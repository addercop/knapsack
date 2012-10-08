#!/usr/bin/python
'''Experimental code that finds the maximum value for a knapsack problem.'''
W = 20
#weight,value pairs.
ITEMS = [(weight, weight * 2) for weight in range(1, 21)]


def get_profit(max_profit, item_count, weight_bound, indent=0):
    '''item_count, index into items. weight_bound, max weight bound.'''
    print " " * indent + "Getting profit for" + str((item_count, weight_bound))
    if item_count <= 0:
        #terminate recursion
        print " " * indent + "item_count was <= 0. returning 0"
        return 0
    if (item_count, weight_bound) in max_profit:
        #already have answer
        print " " * indent + \
            "Already had an answer. returning " \
                + str(max_profit[(item_count, weight_bound)])
        return max_profit[(item_count, weight_bound)]
    w_i = ITEMS[item_count][0]
    v_i = ITEMS[item_count][1]
    if w_i > weight_bound:
        #if this item alone would go overweight.
        max_profit[(item_count, weight_bound)] = \
            get_profit(max_profit, item_count - 1, weight_bound, indent + 1)
        print " " * indent + \
            "This item alone would go overweight. Returning " + \
                str(max_profit[(item_count, weight_bound)])
        return max_profit[(item_count, weight_bound)]
    max_profit[(item_count, weight_bound)] = \
        max(\
            get_profit(max_profit, item_count - 1, weight_bound, indent + 1), \
            get_profit(\
                max_profit, item_count - 1, weight_bound - w_i, indent + 1\
            ) + v_i\
        )
    print " " * indent + "Finally returning " \
        + str(max_profit[(item_count, weight_bound)])
    return max_profit[(item_count, weight_bound)]


def main():
    '''Driver for dynamic programming search for maximum profit.'''
    item_count = len(ITEMS) - 1
    max_profit = {}
    print "Capacity: %d" % W
    print "Items: %s" % str(ITEMS)
    print get_profit(max_profit, item_count, W)

if __name__ == "__main__":
    main()
