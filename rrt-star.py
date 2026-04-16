import math, sys, pygame, random
from math import *
from pygame import *
import numpy as np
import time

class Node(object):
    def __init__(self, point, parent, cost=0):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent
        self.cost = cost

XDIM = 720
YDIM = 500
windowSize = [XDIM, YDIM]
delta = 20.0
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

count = 0
rectObs = []
obs = []

def dist(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def point_circle_collision(p1, p2, radius):
    return dist(p1, p2) <= radius

def step_from_to(p1,p2):
    if dist(p1, p2) < delta:
        return p2
    else:
        theta = atan2(p2[1]-p1[1], p2[0]-p1[0])
        return p1[0] + delta*cos(theta), p1[1] + delta*sin(theta)

def collides(p):
    for rect in rectObs:
        if rect.collidepoint(p):
            return True
    
    return pointCollides(p)

def pointCollides(p):
    for circle in obs:
        cen, rad = circle
        if dist(p, cen) <= rad:
            return True
    return False

def lineCollides(p1, p2, obstacles=None):
    global obs
    if obstacles is None:
        obstacles = obs
    else:
        obstacles = [obstacles]
    a = p2[1] - p1[1]
    b = -(p2[0] - p1[0])
    c = -b * p2[1] - a * p2[0]
    for circle in obstacles:
        cen, rad = circle
        val = (a * cen[0] + b * cen[1] + c * 1.0) / (a * a + b * b)
        val = -val
        h = (val * a) + cen[0]
        k = (val * b) + cen[1]
        if dist(cen,(h,k)) < 1.1*rad:
            if min(p1[0],p2[0]) <= h <= max(p1[0],p2[0]) and min(p1[1],p2[1]) <= k <= max(p1[1],p2[1]):
                return True
    for rect in rectObs:
        if rect.clipline(p1, p2):  # line intersects rectangle
            return True
    return False

def get_random_clear():
    while True:
        p = random.random()*XDIM, random.random()*YDIM
        if not collides(p):
            return p

def init_circular_obstacles(configNum=0):
    global obs
    obs.clear()
    obs.extend([((150,100),18), ((150,130),18), ((150,160),18), ((150,190),18), ((150,220),18),
                ((150,250),18), ((180,250),18), ((210,250),18), ((240,250),18), ((270,250),18),
                ((300,250),18), ((330,250),18), ((330,220),18), ((330,190),18), ((330,160),18),
                ((330,130),18), ((330,100),18), ((300,100),18), ((270,100),18), ((240,100),18),
                ((240,130),18), ((240,160),18), ((240,190),18)])
    for circ in obs:
        pygame.draw.circle(screen, black, circ[0], circ[1])
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
 
def reset():
    global count
    screen.fill(white)
    init_circular_obstacles()
    #init_obstacles1()
    #init_case_3_5_split_obstacles()
    count = 0

def main():
    reset()
    global count
    nodes=[]
    initialPoint = None
    goalPoint = None
    currentState = 'init'
    selecting = True
    while selecting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit("Exiting")
            if e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos
                if not initialPoint:
                    if not collides((x, y)):
                        initialPoint = Node((x, y), None, 0)
                        nodes.append(initialPoint)
                        pygame.draw.circle(screen, red, (x, y), GOAL_RADIUS)
                        print(f"Initial Point Set at: ({x}, {y})")
                elif not goalPoint:
                    if not collides((x, y)):
                        goalPoint = Node((x, y), None, 0)
                        pygame.draw.circle(screen, green, (x, y), GOAL_RADIUS)
                        print(f"Goal Point Set at: ({x}, {y})")
                        selecting = False
        pygame.display.update()
        fpsClock.tick(30)
    currentState = 'buildTree'
    reset()
    pygame.draw.circle(screen, red, initialPoint.point, GOAL_RADIUS)
    pygame.draw.circle(screen, green, goalPoint.point, GOAL_RADIUS)
    start_time = time.time()
    while True:
        if currentState == 'goalFound':
            end_time = time.time()
            total_time = end_time - start_time
            currNode = goalPoint
            pygame.display.set_caption('Goal Reached')
            turns = 0
            while currNode.parent is not None:
                pygame.draw.line(screen, red, currNode.point, currNode.parent.point)
                currNode = currNode.parent
                turns += 1
            print(f"✅ Shortest Distance (Cost): {goalPoint.cost:.2f}")
            print(f"⏱ Time Taken: {total_time:.2f} seconds")
            print(f"🌲 Tree Depth (Nodes): {len(nodes)}")
            print(f"🔁 Number of Turns: {turns}")
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                        sys.exit("Exiting")
                pygame.display.update()
                fpsClock.tick(30)
        elif currentState == 'buildTree':
            count += 1
            pygame.display.set_caption('Performing RRT')
            if count < NUMNODES:
                foundNext = False
                while not foundNext:
                    rand = get_random_clear()
                    parentNode = nodes[0]
                    for p in nodes:
                        if dist(p.point, rand) <= dist(parentNode.point, rand):
                            newPoint = step_from_to(p.point, rand)
                            if not lineCollides(newPoint, p.point) and not pointCollides(newPoint):
                                parentNode = p
                                foundNext = True
                newnode = step_from_to(parentNode.point, rand)
                if dist(parentNode.point, newnode) <= GOAL_RADIUS:
                    continue
                for p in nodes:
                    if dist(p.point, newnode) + p.cost <= dist(parentNode.point, newnode) + parentNode.cost:
                        if not lineCollides(newnode, p.point) and not pointCollides(newnode):
                            parentNode = p
                nodes.append(Node(newnode, parentNode, parentNode.cost + dist(newnode, parentNode.point)))
                if point_circle_collision(newnode, goalPoint.point, GOAL_RADIUS) or lineCollides(newnode, parentNode.point, (goalPoint.point, GOAL_RADIUS)):
                    currentState = 'goalFound'
                    goalPoint.parent = parentNode
                    goalPoint.cost = parentNode.cost + dist(goalPoint.point, parentNode.point)
                else:
                    pygame.draw.line(screen, cyan, parentNode.point, newnode)
            else:
                print("❌ Ran out of nodes. Goal not reached.")
                break
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Exiting")
        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()