#def shortest_path(p1, p2):
    #We'll do Breadth first search, keeping track of profiles that we've
    #   already "visited" so that we don't get stuck in cycles. 

    #Create a list called visited, initially empty, to keep track of the
    #   profiles that we have already visited. This is important for making
    #   sure that we don't get stuck in a cycle in graph. visited will
    #   simply store a list of profile instances

    #Create a list called q, to keep track of the profiles that we have
    #   not yet explored. Initially, q should be a list that contains a tuple
    #   of 3 things - p1 (the starting node), 0 (representing the distance
    #   from that starting node), and p1.name (the beginning of the path).
    #   More generally, each item in q is a list of tuples, each containing -
    #   a profile, the distance from p1 to that profile, and the path from
    #   p1 to that profile, represented as a list of names. For example,
    #   if p1 is sara, then Milan might eventually get added to q as
    #   (milan, 2, ['sara', 'peter', 'milan']).

    #while q is not empty
    #   grab and remove the 0th item from q
    #   this will give you 3 things. Let's call them...
    #      curr - a profile that we are going to examine
    #      dist - the distance from p1 to curr
    #      path - the path from p1 to curr
    #   add curr to visited
    #   if curr is the thing we're looking for (p2)
    #      we're done! Return the two important things (dist and path)
    #   else
    #      for each of curr's connections
    #          if the connection is not already in visited
    #              append a new triple to q
    #                  (the node itself,
    #                  the distance from p1 to that node - computed from dist,
    #                  the path from p1 to that node - computed from path)
    #If we hit this point, we never returned an answer. This means that we should
    #    return None because there is no path between p1 and p2. 


