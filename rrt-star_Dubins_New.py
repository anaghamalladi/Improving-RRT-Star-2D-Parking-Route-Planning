import math, sys, pygame, random
from math import *
from pygame import *
import sys
import random
import math
import copy
import time
import numpy as np
import dubins_path_planning
import matplotlib.pyplot as plt


XDIM = 720
YDIM = 500
windowSize = [XDIM, YDIM]
delta = 10.0
GAME_LEVEL = 1
GOAL_RADIUS = 10
MIN_DISTANCE_TO_ADD = 1.0
NUMNODES = 5000
FPS = 1000
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(windowSize)
white = 255, 255, 255
black = 25, 25, 25
red = 255, 0, 0
blue = 0, 128, 0
green = 0, 0, 255
cyan = 0,180,105
yellow = 255, 255, 0

show_animation = True
STEP_SIZE = 2
curvature = 10

count = 0
obs = []
rectObs = []

def dist(p1,p2):    #distance between two points
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def point_circle_collision(p1, p2, radius):
    distance = dist(p1,p2)
    if (distance <= radius):
        return True
    return False

def step_from_to(p1,p2):
    if dist(p1,p2) < delta:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + delta*cos(theta), p1[1] + delta*sin(theta)
    
def collides(p):    #check if point collides with the obstacle
    
    for circle in obs:
        if len(circle) == 3:  # avoid errors from incorrect obs tuples
            ox, oy, rad = circle
            if dist(p, (ox, oy)) <= rad:
                return True

    # Check rectangular obstacles
    for rect in rectObs:
        if rect.collidepoint(p):
            return True

    return False

def init_obstacles(configNum):  #initialized the obstacle
    global obs
    obs = []
    obs.append((150,100,18))
    obs.append((150,130,18))
    obs.append((150,160,18))
    obs.append((150,190,18))
    obs.append((150,220,18))
    obs.append((150,250,18))
    obs.append((180,250,18))
    obs.append((210,250,18))
    obs.append((240,250,18))
    obs.append((270,250,18))
    obs.append((300,250,18))
    obs.append((330,250,18))
    obs.append((330,220,18))
    obs.append((330,190,18))
    obs.append((330,160,18))
    obs.append((330,130,18))
    obs.append((330,100,18))
    obs.append((300,100,18))
    obs.append((270,100,18))
    obs.append((240,100,18))
    obs.append((240,130,18))
    obs.append((240,160,18))
    obs.append((240,190,18))
    for (ox, oy, size) in obs:
            #plt.plot(ox, oy, "ok", ms=30 * size)
            pygame.draw.circle(screen, black, (ox, oy), size)

def init_obstacles1(configNum=1):
    global rectObs
    rectObs = []

    # Obstacle 1: Top-left rectangle
    rectObs.append(pygame.Rect((100, 50), (200, 150)))

    # Obstacle 2: Bottom-right rectangle
    rectObs.append(pygame.Rect((400, 200), (200, 100)))

    for rect in rectObs:
        pygame.draw.rect(screen, black, rect) 

def init_case_3_5_split_obstacles():
    global rectObs
    rectObs = []

    screen.fill(white)

    # Outer walls
    margin = 10
    pygame.draw.rect(screen, black, (0, 0, XDIM, margin))  # Top wall
    pygame.draw.rect(screen, black, (0, YDIM - margin, XDIM, margin))  # Bottom wall
    pygame.draw.rect(screen, black, (0, 0, margin, YDIM))  # Left wall
    pygame.draw.rect(screen, black, (XDIM - margin, 0, margin, YDIM))  # Right wall

    # Height partitions
    top_2_5 = int((2 / 5) * YDIM)

    # First obstacle (left): top to 2/5 of screen
    rect1 = pygame.Rect((200, 0), (60, top_2_5))

    # Second obstacle (right): from 2/5 to bottom
    rect2 = pygame.Rect((460, top_2_5), (60, YDIM - top_2_5))

    rectObs.extend([rect1, rect2])

    for rect in rectObs:
        pygame.draw.rect(screen, black, rect)


parking_lot_initialized = False 

def init_obstacles_parkingLot1(configNum):  #initialized the obstacle
    global obs,empty_spaces,parking_lot_initialized

    if parking_lot_initialized:
        return 
    
    obs = []
    empty_spaces = []
    parking_start_x = 200  # X-coordinate for the first parking space
    parking_start_y = 150  # Y-coordinate for the first row
    parking_space_width = 60  # Width between parking spots
    parking_space_height = 40  # Distance between two rows
    parking_size = 30  # Obstacle size to simulate parked cars


    entry_point = (parking_start_x - 60, parking_start_y + 20)  # Entry is left of the first row
    exit_point = (parking_start_x + (5 * parking_space_width) + 40, parking_start_y + 20)  # Exit is right of the last row
    
    
    # Add entry and exit markers
    pygame.draw.circle(screen, green, entry_point, 15)  # Green Circle (Entry)
    pygame.draw.circle(screen, red, exit_point, 15)  # Red Circle (Exit)

    # 🅿️ Generate a 2x5 Parking Lot with Random Empty Spaces
    num_empty_spaces = random.randint(8, 9)  # Randomly make 1-3 spaces empty
    empty_indices = random.sample(range(10), num_empty_spaces)  # Randomly pick empty spots

    parking_spaces = []  # Store all possible parking spots

    for row in range(2):  # 2 rows
        for col in range(5):  # 5 columns
            ox = parking_start_x + col * parking_space_width
            oy = parking_start_y + row * parking_space_height

            index = row * 5 + col  # Unique index for each space

            if index in empty_indices:
                empty_spaces.append((ox, oy))  # Save the empty spot
            else:
                obs.append((ox, oy, parking_size))  # Add an occupied parking space

            parking_spaces.append((ox, oy))



    parking_lot_initialized = True


    # 🚗 Draw the occupied spaces (black circles) and mark empty spots (blue circles)
    for (ox, oy, size) in obs:
        pygame.draw.circle(screen, black, (ox, oy), size)  # Occupied spot

    for (ex, ey) in empty_spaces:
        pygame.draw.circle(screen, yellow, (ex, ey), 15)  # Empty parking space

def init_obstacles_parkingLot(configNum):
    """
    Initialize a structured shopping mall-style parking lot with a 2x5 row parking layout filling the entire lot,
    including one-way driving lanes, ensuring everything fits within the screen.
    """
    global obs, empty_spaces, parking_lot_initialized

    if parking_lot_initialized:
        return

    obs = []
    empty_spaces = []
    screen_width, screen_height = 720, 500  # Ensuring full visibility
    parking_start_x = 50
    parking_start_y = 50
    parking_space_width = 45  # Adjusted to fit better
    parking_space_height = 80  # Proper spacing
    parking_size = 28  # More visible parked cars
    num_rows = 4  # Adjusted to fit within screen height
    num_cols = 10  # Maintained structured 2x5 layout
    num_lots = 2  # Adjusted to prevent overflow
    lane_width = 50  # Space for driving lanes
    divider_width = 60  # Pedestrian walkways

    entry_x = parking_start_x - 40
    entry_y = parking_start_y + (num_rows * (parking_space_height + lane_width)) // 2
    exit_x = screen_width - 40
    exit_y = entry_y

    pygame.draw.circle(screen, green, (entry_x, entry_y), 15)  # Entry
    pygame.draw.circle(screen, red, (exit_x, exit_y), 15)  # Exit

    for lot in range(num_lots):
        lot_offset_x = lot * (num_cols * parking_space_width + divider_width)
        num_empty_spaces = random.randint(5, 7)
        empty_indices = random.sample(range(num_rows * num_cols), num_empty_spaces)

        for row in range(num_rows):
            for col in range(num_cols):
                ox = parking_start_x + col * parking_space_width + lot_offset_x
                oy = parking_start_y + row * (parking_space_height + lane_width)

                # Opposite row parking: Flip direction every other row
                if row % 2 == 1:
                    ox = parking_start_x + (num_cols - 1 - col) * parking_space_width + lot_offset_x
                    oy += parking_space_height // 4  # Adjusted for spacing
                
                index = row * num_cols + col
                if index in empty_indices:
                    empty_spaces.append((ox, oy))
                else:
                    obs.append((ox, oy, parking_size))

    parking_lot_initialized = True

    # Draw parked cars and empty spaces with better structure
    for (ox, oy, size) in obs:
        pygame.draw.circle(screen, black, (ox, oy), size)
    for (ex, ey) in empty_spaces:
        pygame.draw.circle(screen, yellow, (ex, ey), 15)  # Clear empty spaces

    # Draw one-way lane indicators using arrows
    for lot in range(num_lots):
        lot_offset_x = lot * (num_cols * parking_space_width + divider_width)
        for row in range(num_rows):
            lane_x = parking_start_x + (num_cols // 2) * parking_space_width + lot_offset_x
            lane_y = parking_start_y + row * (parking_space_height + lane_width) + (parking_space_height // 2)
            pygame.draw.polygon(screen, (0, 0, 255), [(lane_x, lane_y - 8), (lane_x + 8, lane_y), (lane_x, lane_y + 8)])

def init_obstacles_parallelParking(configNum):
    """
    Initialize a structured parallel parking layout along a road lane between houses.
    The car should park itself in an empty parallel parking spot using the Dubins path algorithm.
    """
    global obs, empty_spaces

    if 'empty_spaces' not in globals():
        empty_spaces = []
    
    screen_width, screen_height = 720, 500  # Ensuring full visibility
    road_start_x = 50
    road_start_y = screen_height // 2 - 30  # Center the road
    road_width = 100  # Width of the road lane
    parking_space_length = 80  # Length of each parallel parking spot
    parking_space_width = 30  # Width of each spot
    num_spaces = 5  # Number of parallel parking spots on each side
    lane_gap = 15  # Space between parallel parking and road lane

    num_empty_spaces = random.randint(2, 3)  # Random empty spots per side
    empty_indices_left = random.sample(range(num_spaces), num_empty_spaces)
    empty_indices_right = random.sample(range(num_spaces), num_empty_spaces)

    # Draw the road
    pygame.draw.rect(screen, (50, 50, 50), (road_start_x, road_start_y, screen_width - 100, road_width))

    # Parallel parking spots on the left side
    for i in range(num_spaces):
        px = road_start_x + i * (parking_space_length + lane_gap)
        py = road_start_y - parking_space_width - 10  # Positioning above the road

        if i in empty_indices_left:
            empty_spaces.append((px, py))
        else:
            obs.append((px, py, parking_space_width))

    # Parallel parking spots on the right side
    for i in range(num_spaces):
        px = road_start_x + i * (parking_space_length + lane_gap)
        py = road_start_y + road_width + 10  # Positioning below the road

        if i in empty_indices_right:
            empty_spaces.append((px, py))
        else:
            obs.append((px, py, parking_space_width))

    # Draw parked cars and empty spaces on both sides
    for (px, py, size) in obs:
        pygame.draw.rect(screen, black, (px, py, parking_space_length, size))
    for (ex, ey) in empty_spaces:
        pygame.draw.rect(screen, yellow, (ex, ey, parking_space_length, parking_space_width))  # Mark empty spots

    # Draw houses as obstacles
    house_width = 60
    house_height = 80
    house_gap = 30
    for i in range(num_spaces):
        hx_left = road_start_x + i * (parking_space_length + lane_gap)
        hy_left = road_start_y - parking_space_width - house_height - 20
        pygame.draw.rect(screen, (150, 75, 0), (hx_left, hy_left, house_width, house_height))
        obs.append((hx_left + house_width // 2, hy_left + house_height // 2, house_width // 2))

        hx_right = road_start_x + i * (parking_space_length + lane_gap)
        hy_right = road_start_y + road_width + parking_space_width + 20
        pygame.draw.rect(screen, (150, 75, 0), (hx_right, hy_right, house_width, house_height))
        obs.append((hx_right + house_width // 2, hy_right + house_height // 2, house_width // 2))
    
    # Make the car park in the closest empty spot using Dubins path (forward motion only)
    if empty_spaces:
        car_start_x, car_start_y = road_start_x + 20, road_start_y + road_width // 2
        car_start_yaw = 0  # Initial heading direction

        car_goal_x, car_goal_y = empty_spaces[0]  # Assign car to the first available empty spot
        car_goal_y += parking_space_width // 2  # Center it in the space
        car_goal_yaw = np.deg2rad(90)  # Face the parking spot

        turning_radius = 2.0  # Adjust based on vehicle properties

        # Compute Dubins path
        path_result = dubins_path_planning.dubins_path_planning(
            car_start_x, car_start_y, car_start_yaw, 
            car_goal_x, car_goal_y, car_goal_yaw, 
            turning_radius
        )

        # Check if the path is valid before extracting coordinates
        if isinstance(path_result, tuple) and len(path_result) == 3:
            px, py, pyaw = path_result  # Unpack the Dubins path result

            # Draw car movement path
            for i in range(1, len(px)):
                pygame.draw.line(screen, blue, (px[i - 1], py[i - 1]), (px[i], py[i]), 2)  # Blue path

            pygame.draw.rect(screen, blue, (car_goal_x, car_goal_y, parking_space_length, parking_space_width))  # Draw parked car

            # Convert all other empty spaces into obstacles after parking
            empty_spaces.remove((car_goal_x, car_goal_y))
            for (ex, ey) in empty_spaces:
                obs.append((ex + parking_space_length // 2, ey + parking_space_width // 2, parking_space_width // 2))
        else:
            print("Error: Dubins path did not return expected format.")



def reset():
    global count
    screen.fill(white)
    #init_obstacles(GAME_LEVEL)
    #init_obstacles1()
    #init_case_3_5_split_obstacles()
    #init_obstacles_parkingLot1(GAME_LEVEL)
    #init_obstacles_parkingLot(GAME_LEVEL)
    init_obstacles_parallelParking(GAME_LEVEL)
    
    count = 0

class RRT():
    """
    Class for RRT Planning
    """

    def __init__(self, start, goal, obstacleList, randArea,
                 goalSampleRate=10, maxIter=120):
        """
        Setting Parameter
        start:Start Position [x,y]
        goal:Goal Position [x,y]
        obstacleList:obstacle Positions [[x,y,size],...]
        randArea:Ramdom Samping Area [min,max]
        """
        self.start = Node(start[0], start[1], start[2])
        self.end = Node(goal[0], goal[1], goal[2])
        self.minrand = randArea[0]
        self.maxrand = randArea[1]
        self.goalSampleRate = goalSampleRate
        self.maxIter = maxIter
        self.obstacleList = obstacleList

    def Planning(self, animation=True):
        """
        Pathplanning
        animation: flag for animation on or off
        """

        self.nodeList = [self.start]
        for i in range(self.maxIter):
            if(i%10==0):
                print("Planning path",i)
			
            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                    sys.exit("Exiting")

            rnd = self.get_random_point()
            nind = self.GetNearestListIndex(self.nodeList, rnd)

            newNode = self.steer(rnd, nind)
            if newNode is None:
                continue

            if self.CollisionCheck(newNode, self.obstacleList):
                nearinds = self.find_near_nodes(newNode)
                newNode = self.choose_parent(newNode, nearinds)
                if newNode is None:
                    continue
                self.nodeList.append(newNode)
                self.rewire(newNode, nearinds)

            if animation and i % 5 == 0:
                self.DrawGraph(rnd=rnd)
            #if(newNode.)

        # generate coruse
        lastIndex = self.get_best_last_index()
        if lastIndex is None:
            return None
        path = self.gen_final_course(lastIndex)
        print("Path planning done")
        return path

    def choose_parent(self, newNode, nearinds):
        if len(nearinds) == 0:
            return newNode

        dlist = []
        valid_indices = []  # Store indices of valid parents

        for i in nearinds:
            tNode = self.steer(newNode, i)
            if tNode is None:
                continue

            if self.CollisionCheck(tNode, self.obstacleList):
                dlist.append(tNode.cost)
                valid_indices.append(i)  # Keep track of valid indices
        if not dlist:  # If no valid parents found
            print("Warning: No valid parent found for the node.")
            return None  # Prevents empty min() call    

        mincost = min(dlist)
        minind = nearinds[dlist.index(mincost)]

        return self.steer(newNode, minind)  # Return the best valid parent

        if mincost == float("inf"):
            print("mincost is inf")
            return newNode

        newNode = self.steer(newNode, minind)

        return newNode

    def pi_2_pi(self, angle):
        return (angle + math.pi) % (2 * math.pi) - math.pi

    def steer(self, rnd, nind):

        nearestNode = self.nodeList[nind]

        px, py, pyaw, mode, clen = dubins_path_planning.dubins_path_planning(
            nearestNode.x, nearestNode.y, nearestNode.yaw, rnd.x, rnd.y, rnd.yaw, curvature)

        if px is None:
            
            return None

        newNode = copy.deepcopy(nearestNode)
        newNode.x = px[-1]
        newNode.y = py[-1]
        newNode.yaw = pyaw[-1]

        newNode.path_x = px
        newNode.path_y = py
        newNode.path_yaw = pyaw
        newNode.cost += clen
        newNode.parent = nind

        

        #for (ox, oy, size) in self.obstacleList:
            #for (ix, iy) in zip(px, py):
                #if (ix - ox) ** 2 + (iy - oy) ** 2 <= size ** 2:
                    #print("🚫 Invalid Dubins path: Car would collide with obstacles.")
                    #return None  # Reject the path if it collides

    # **🚨 Ensure Dubins Doesn't Cross Over Obstacles**
       # for i in range(len(px) - 1):
            #if any(self.CollisionCheck(Node(px[i], py[i], pyaw[i]), self.obstacleList) for i in range(len(px))):
                #print("🚫 Invalid Dubins path: Unrealistic movement detected.")
                #return None  # Reject unrealistic paths

        return newNode  # Return the valid node

    def get_random_point(self):

        if random.randint(0, 100) > self.goalSampleRate:
            rnd = [random.uniform(self.minrand, self.maxrand),
                   random.uniform(self.minrand, self.maxrand),
                   random.uniform(-math.pi, math.pi)
                   ]
        else:  # goal point sampling
            rnd = [self.end.x, self.end.y, self.end.yaw]

        node = Node(rnd[0], rnd[1], rnd[2])

        return node

    def get_best_last_index(self):
        #  print("get_best_last_index")

        YAWTH = np.deg2rad(3.0)
        XYTH = 0.5

        goalinds = []
        for (i, node) in enumerate(self.nodeList):
            if self.calc_dist_to_goal(node.x, node.y) <= XYTH:
                goalinds.append(i)
        #  print("OK XY TH num is")
        #  print(len(goalinds))

        # angle check
        fgoalinds = []
        for i in goalinds:
            if abs(self.nodeList[i].yaw - self.end.yaw) <= YAWTH:
                fgoalinds.append(i)
        #  print("OK YAW TH num is")
        #  print(len(fgoalinds))

        if len(fgoalinds) == 0:
            return None

        mincost = min([self.nodeList[i].cost for i in fgoalinds])
        for i in fgoalinds:
            if self.nodeList[i].cost == mincost:
                return i

        return None

    def gen_final_course(self, goalind):
        path = [[self.end.x, self.end.y]]
        while self.nodeList[goalind].parent is not None:
            node = self.nodeList[goalind]
            for (ix, iy) in zip(reversed(node.path_x), reversed(node.path_y)):
                path.append([ix, iy])
            #  path.append([node.x, node.y])
            goalind = node.parent
        path.append([self.start.x, self.start.y])
        return path

    def calc_dist_to_goal(self, x, y):
        return np.linalg.norm([x - self.end.x, y - self.end.y])

    def find_near_nodes(self, newNode):
        nnode = len(self.nodeList)
        r = 50.0 * math.sqrt((math.log(nnode) / nnode))
        #  r = self.expandDis * 5.0
        dlist = [(node.x - newNode.x) ** 2 +
                 (node.y - newNode.y) ** 2 +
                 (node.yaw - newNode.yaw) ** 2
                 for node in self.nodeList]
        nearinds = [dlist.index(i) for i in dlist if i <= r ** 2]
        return nearinds

    def rewire(self, newNode, nearinds):

        nnode = len(self.nodeList)

        for i in nearinds:
            nearNode = self.nodeList[i]
            tNode = self.steer(nearNode, nnode - 1)
            if tNode is None:
                continue

            obstacleOK = self.CollisionCheck(tNode, self.obstacleList)
            imporveCost = nearNode.cost > tNode.cost

            if obstacleOK and imporveCost:
                #  print("rewire")
                self.nodeList[i] = tNode

    def DrawGraph(self, rnd=None):
        """
        Draw Graph
        """
        reset()
        if rnd is not None:
            plt.plot(rnd.x, rnd.y, "^k")
        for node in self.nodeList:
            if node.parent is not None:
                plt.plot(node.path_x, node.path_y, "-g")
                for i in range(1, len(node.path_x)):
                    pygame.draw.line(screen,blue,(node.path_x[i-1], node.path_y[i-1]), (node.path_x[i], node.path_y[i]))
                #  plt.plot([node.x, self.nodeList[node.parent].x], [
                #  node.y, self.nodeList[node.parent].y], "-g")

        for (ox, oy, size) in self.obstacleList:
            #plt.plot(ox, oy, "ok", ms=30 * size)
            pygame.draw.circle(screen, black, (ox, oy), size)

        '''reeds_shepp_path_planning.plot_arrow(self.start.x, self.start.y, self.start.yaw)
        reeds_shepp_path_planning.plot_arrow(self.end.x, self.end.y, self.end.yaw)'''
        pygame.draw.circle(screen, red, (self.start.x, self.start.y), GOAL_RADIUS)
        pygame.draw.circle(screen, green, (self.end.x, self.end.y), GOAL_RADIUS)

        '''plt.axis([-2, 15, -2, 15])
        plt.grid(True)
        plt.pause(0.01)'''
        pygame.display.update()
        #  plt.show()
        #  input()

    def GetNearestListIndex(self, nodeList, rnd):
        dlist = [(node.x - rnd.x) ** 2 +
                 (node.y - rnd.y) ** 2 +
                 (node.yaw - rnd.yaw) ** 2 for node in nodeList]
        minind = dlist.index(min(dlist))

        return minind

    #def CollisionCheck(self, node, obstacleList):

        for (ox, oy, size) in obstacleList:
            for (ix, iy) in zip(node.path_x, node.path_y):
                dx = ox - ix
                dy = oy - iy
                d = dx * dx + dy * dy
                if d <= size ** 2:
                    return False  # collision

        return True  # safe
    
    def CollisionCheck(self, node, obstacleList):
        for (ix, iy) in zip(node.path_x, node.path_y):
            if collides((ix, iy)):
                return False  # Path collides with an obstacle
        return True  # Safe path


class Node():
    """
    RRT Node
    """

    def __init__(self, x, y, yaw):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.path_x = []
        self.path_y = []
        self.path_yaw = []
        self.cost = 0.0
        self.parent = None

def is_inside_circle(goal_x, goal_y, circle_x, circle_y, radius=25):
    """Check if the goal point lies within a circle centered at (circle_x, circle_y)"""
    return (goal_x - circle_x) ** 2 + (goal_y - circle_y) ** 2 <= radius ** 2


def main():
    global count
    
    ##  this is for mouse click ####
    initPoseSet = False
    initialPoint = Node(None, None, 0)
    goalPoseSet = False
    goalPoint = Node(None, None, 0)
    currentState = 'init'
    #############################

    ## this is for manually setting the points####
    #initialPoint = Node(138, 168, np.deg2rad(0.0))
    #goalPoint = Node(205, 183, np.deg2rad(0.0))

    print(f" Initial Point Set at: ({initialPoint.x}, {initialPoint.y})")
    print(f" Goal Point Set at: ({goalPoint.x}, {goalPoint.y})")

    #currentState = 'buildTree'
    
    
    rrt = None
    path = None

    nodes = []
    reset()

    while True:
        if currentState == 'init':
            pygame.display.set_caption('Select Starting Point and then Goal Point')
            fpsClock.tick(10)
        elif currentState == 'goalFound':
            end_time = time.time()
            total_time = end_time - start_time
            
            currNode = goalPoint
            pygame.display.set_caption('Goal Reached')
            
            while currNode.parent is not None:
                turns += 1
                currNode = currNode.parent
            rrt.DrawGraph()
            for i in range(1, len(path)):
                pygame.draw.line(screen, red, path[i-1], path[i])
            optimizePhase = True
        elif currentState == 'optimize':
            fpsClock.tick(0.5)
            pass
        elif currentState == 'buildTree':
            ## from empty spaces select all the other spots which are not the goal and mark them as obstacles
            #for (ex, ey) in empty_spaces:
                #if not is_inside_circle(goalPoint.x, goalPoint.y, ex, ey, radius=25):  
                    #obs.append((ex, ey, 25))  # Mark as an obstacle

            #print(" Other empty spaces have been converted into obstacles.")

            rrt = RRT((initialPoint.x, initialPoint.y, initialPoint.yaw), (goalPoint.x, goalPoint.y, goalPoint.yaw), randArea=[0, 500], obstacleList=obs)
            start_time = time.time()
            path = rrt.Planning(True)
            end_time = time.time()
            elapsed_time = end_time - start_time
            if(path != None):
                total_distance = sum(dist(path[i], path[i + 1]) for i in range(len(path) - 1))
                currentState = 'goalFound'
                turns = len(path) - 1  # number of path segments
                tree_depth = len(rrt.nodeList)
                print(f" Shortest Path Found in: {elapsed_time:.4f} seconds")
                print(f" Shortest Path Distance: {total_distance:.2f} units")
                print(f"🌲 Tree Depth (Nodes): {len(nodes)}")
                print(f"🔁 Number of Turns: {turns}")


        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Exiting")
            if e.type == MOUSEBUTTONDOWN:
                print('mouse down')
                if currentState == 'init':
                    if initPoseSet == False:
                        nodes = []
                        if collides(e.pos) == False:
                            print('initiale point set: '+str(e.pos))

                            initialPoint = Node(e.pos[0], e.pos[1], np.deg2rad(0.0))
                            initPoseSet = True
                            pygame.draw.circle(screen, red, (initialPoint.x, initialPoint.y), GOAL_RADIUS)
                    elif goalPoseSet == False:
                        print('goal point set: '+str(e.pos))
                        if collides(e.pos) == False:
                            goalPoint = Node(e.pos[0], e.pos[1], np.deg2rad(90.0))
                            goalPoseSet = True
                            pygame.draw.circle(screen, green, (goalPoint.x, goalPoint.y), GOAL_RADIUS)
                            #pygame.display.update()
                            currentState = 'buildTree'
                else:
                    currentState = 'init'
                    initPoseSet = False
                    goalPoseSet = False
                    reset()

        pygame.display.update()
        fpsClock.tick(FPS)



if __name__ == '__main__':
    main()
    
