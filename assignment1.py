import math

def restaurantFinder(d, site_list):
    """
    Function description: This function determines which sites should be opened that can also maximise the overall revenue, given that there must be a
    certain distance between each site.

    Approach description: The algorithm will iterate over the values of site_list, which are the annual revenues of each site. If that site is selected,
    then its revenue will be added to the total. If the next site to be visited is not d km apart from the previous opened site, then the total revenue
    from the previous site will not be updated. If the next site is d km apart and will maximise the profit, then its revenue will be added and the 
    total revenue will be updated. The algorithm will then check for any alternate combinations that may yield a higher total revenue than the current 
    combination and update the total revenue. Once the optimal total revenue is found, we take the index of each of the individual annual revenues in its 
    original site_list and add 1 to output the selected sites' numbers.

    Inputs:
        - d: an integer representing the minimum distance (in km) between two restaurant sites  
        - site_list: a list of values which represents the annual revenue (in million dollars) 

    Outputs:
        - a tuple containing total_revenue (maximised total revenue of the sites which will be opened) and selected_sites, a list of the selected sites.

    Given that n is number of sites in site_list: 
    - Time complexity: O(n). As the function is iterating over the list and processing each site once, making the worst-case time complexity linear. Other 
    operations such as updating variables and adding values to the total value will all be done in O(1) time.
    - Space complexity: O(n). The function requires space to store the n numbers of sites in selected_sites, while other values such as distance, size,
    prediction, pointer and total revenue take up constant space even if the value is large.
    """
    distance = d+1
    size = len(site_list)
    prediction = math.ceil(size / distance) 
    pointer = 0
    total_revenue = 0
    selected_sites = []

    while pointer < size:
        next = size - pointer # no. of sites left to be considered
        if next > distance: # more potential sites remain
            next = distance
            current_revenue = site_list[pointer] + site_list[pointer+distance] # next site is selected
        else:
            next = size - pointer
            current_revenue = site_list[pointer] # next site will not add to revenue

        current_site = pointer    
        
        # check if there can be better combinations
        for i in range(next): 
            remaining_sites = len(selected_sites) + math.ceil((size-i-pointer) / distance)
            if remaining_sites == prediction:
                check = site_list[pointer + i] # access site that is i distance away
                if check > current_revenue: # current combination is best 
                    current_site = pointer + 1
                    if i + pointer + distance < size:
                        current_revenue = check + site_list[i+pointer+distance]
                    else:
                        current_revenue = check # if new combination is better, update
            else: # current combination is already the best so adding the current site will not improve it
                check = site_list[i+pointer]
                if check >= current_revenue:
                    current_site = i + pointer
                    prediction = remaining_sites
        
        # adding the sites to final selected sites
        selected_sites.append(current_site + 1)
        pointer = current_site
        total_revenue += site_list[current_site] # add to total revenue
        pointer += distance # move to next potential site 

    return (total_revenue, selected_sites)

# sample input and output
result1 = restaurantFinder(1,[50,10,12,65,40,95,100,12,20,30])
print(result1)


class FloorGraph:
    def __init__(self, paths, keys):
        """
        Function description: This function initialises a graph which represents the floor map as a list, where the vertices represent a location and the 
        edges connect locations to each other. The edge weights represents the time in minutes it would take to traverse between the two vertices it joins. 
        This function also stores the keys at certain locations of the floor map in a list.

        Approach description: The function initialises an empty list to the length of the maximum value found in the paths list and the keys list is 
        initialised with a length of the maximum value in the input keys list, with all values set to None. Using for loops, the values of the graph and 
        the keys will be added to their own lists respectively.
        
        Inputs: 
            - paths: a list of tuples (u,v,x) where u is the starting location ID, v is the ending location ID and x is the amount of time taken to travel
            from u to v. All three values are non-negative integers.
            - keys: a list of tuples (k,y) where k is the location ID where a key can be found and y is the time taken to defeat the monster if we decide
            to collect the key at that location. Both k and y are non-negative integers.

        Outputs: 
            - None
        
        Given that V is the set of unique locations in the map and E is the set of paths:
        - Time complexity: O(|V|+|E|). There are two seperate for loops, one which iterates through each location and its paths and one which iterates over
        all the keys. Since the second loop which also has a linear worst-case time complexity of O(|V|), the overall time taken is O(|V|+|E|).
        - Space complexity: O(|V|+|E|). The self.graph data is the dominant factor as it contains the V locations and E paths of the floor map while 
        self.keys is only O(|V|).
        """ 
        self.max_path_value = 0
        self.max_key_value = 0

        for u, v, x in paths:
            self.max_path_value = max(self.max_path_value, u, v)

        for k, y in keys:
            self.max_key_value = max(self.max_key_value, k)

        max_value = max(self.max_path_value, self.max_key_value)

        # initialise the graph data structure using lists
        self.graph = [[] for _ in range(max_value + 1)] # empty list
        self.keys = [None] * (max_value + 1) # all initialised to None

        # populate the graph with paths
        for u, v, x in paths:
            self.graph[u].append((v, x))

        # populate the keys information
        for k, y in keys:
            self.keys[k] = y

    def get_paths(self, location):
        """
        This function retrieves the paths at a certain location ID.

        Inputs: 
            - location: an integer which represents the location's ID
        
        Outputs: 
            - a list of paths which can be traversed from that location
        """
        return self.graph[location]

    def get_key_defense_time(self, location):
        """
        This function retrieves the key at a certain location ID.

        Inputs: 
            - location: an integer which represents the location's ID
        
        Outputs: 
            - an integer which is the key found at that location.
        """
        return self.keys[location]

    def climb(self, start, exits):
        """
        Function description: This function will find the path that can traverse from the start to an exit while also collecting a key which can take us
        to the next floor of the tower. 

        Approach description: As there are no negative edge weights, this function implements a modidied version of Dijkstra's algorithm for finding the
        shortest path (the path which takes the least amount of time). It is modified to find a key and be able to return the route which was taken from
        the start to an exit. Similar to Dijkstra's, we visit each node and check the path with the shortest time and reconstruct the route by adding the 
        paths chosen. We then relax each path until we find the quickest route.

        Inputs:
            - start: a non-negative integer which represents the location ID of the starting position
            - exists: a non-empty list of non-negative integers, each representing the location ID at which an exit is located

        Outputs:
            - total_time: a non-negative integer which represents the time taken (in minutes) to traverse the paths from the start to an exit while also
            collecing a key along the way
            - route: a list of integers that represents the order in which locations were visited
        
        Given that V is the set of unique locations in the map and E is the set of paths:
        - Time complexity: O(V+E). In the worst case, each location in the floor map graph is visited once and each edge is relaxed once, since the 
        inner loop will iterate through the neighbours (adjacent vertices) of the current location. 
        - Space complexity: O(V+E). Space is required to store the locations visited as well as the paths which were traversed to travel from the start
        to an exit. Other values such as current_location (the current location being processed) and min_time (the minimum time taken to traverse from 
        start to an exit) only take up O(1) space.
        """
        shortest_path = [float('inf')] * len(self.graph)
        shortest_path[start] = 0
        visited = [False] * len(self.graph)

        while True:
            min_time = float('inf') 
            current_location = None
            # selects the unvisited node with shortest time (represented by edge weights)
            for location in range(len(shortest_path)):
                if not visited[location] and shortest_path[location] < min_time: 
                    min_time = shortest_path[location]
                    current_location = location

            if current_location is None:
                return None

            visited[current_location] = True # no more unvisited locations
            
            # reconstruct path
            if current_location in exits: 
                route = []
                total_time = shortest_path[current_location]

                while current_location != start:
                    route.append(current_location) 
                    for neighbor, path_time in self.graph[current_location]:
                        if shortest_path[current_location] == shortest_path[neighbor] + path_time:
                            current_location = neighbor
                            break

                route.append(start)
                route.reverse()

                return total_time, route

            # path relaxation       
            for neighbor, path_time in self.graph[current_location]:
                key_defense_time = self.get_key_defense_time(neighbor)
                if shortest_path[current_location] + path_time < shortest_path[neighbor]: 
                    if key_defense_time is not None:
                        shortest_path[neighbor] = shortest_path[current_location] + path_time + key_defense_time # relax path
                    else:
                        shortest_path[neighbor] = shortest_path[current_location] + path_time # decided not to fight monster for the key

# sample input and output
paths = [(0, 1, 4), (0, 3, 2), (0, 2, 3), (2, 3, 2), (3, 0, 3)]
keys = [(0, 5), (3, 2), (1, 3)]
start = 1
exits = [7, 2, 4]

myfloor = FloorGraph(paths, keys)
result2 = myfloor.climb(start, exits)
print(result2)
