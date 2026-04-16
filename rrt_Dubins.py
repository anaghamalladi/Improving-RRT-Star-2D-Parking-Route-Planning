import math, sys, pygame, random
import numpy as np
import dubins_path_planning

class Node:
    def __init__(self, x, y, yaw=0.0):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.path_x = []
        self.path_y = []
        self.path_yaw = []
        self.cost = 0.0
        self.parent = None

XDIM, YDIM = 720, 500
GOAL_RADIUS = 10
NUMNODES = 5000
FPS = 1000
curvature = 1.0

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((XDIM, YDIM))

white = 255, 255, 255
black = 25, 25, 25
red = 255, 0, 0
green = 0, 255, 0
cyan = 0, 180, 105

obs = []
def dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
    rectObs= []
def collides(p):
    for circle in obs:
        cen, rad = circle
        if dist(p, cen) <= rad:
            return True
    for rect in rectObs:
        if rect.collidepoint(p):
            return True
    return False

def dubins_steer(from_node, to_node):
    px, py, pyaw, mode, clen = dubins_path_planning.dubins_path_planning(
        from_node.x, from_node.y, from_node.yaw,
        to_node.x, to_node.y, to_node.yaw,
        curvature
    )
    if px is None:
        return None

    # Collision check along Dubins path
    for (x, y) in zip(px, py):
        if collides((x, y)):
            return None

    new_node = Node(px[-1], py[-1], pyaw[-1])
    new_node.path_x = px
    new_node.path_y = py
    new_node.path_yaw = pyaw
    new_node.cost = from_node.cost + clen
    new_node.parent = from_node
    return new_node

def get_random_clear():
    start_time = time.time()
    while True:
        x = random.uniform(0, XDIM)
        y = random.uniform(0, YDIM)
        if not collides((x, y)):
            yaw = random.uniform(-math.pi, math.pi)
            return Node(x, y, yaw)

def init_obstacles():
    global obs
    obs.clear()
    obs.append(((150,100),18))
    obs.append(((150,130),18))
    obs.append(((150,160),18))
    obs.append(((150,190),18))
    obs.append(((150,220),18))
    obs.append(((150,250),18))
    obs.append(((180,250),18))
    obs.append(((210,250),18))
    obs.append(((240,250),18))
    obs.append(((270,250),18))
    obs.append(((300,250),18))
    obs.append(((330,250),18))
    obs.append(((330,220),18))
    obs.append(((330,190),18))
    obs.append(((330,160),18))
    obs.append(((330,130),18))
    obs.append(((330,100),18))
    obs.append(((300,100),18))
    obs.append(((270,100),18))
    obs.append(((240,100),18))
    obs.append(((240,130),18))
    obs.append(((240,160),18))
    obs.append(((240,190),18))
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

def draw_path(node):
    while node.parent is not None:
        for i in range(1, len(node.path_x)):
            pygame.draw.line(screen, red, (node.path_x[i - 1], node.path_y[i - 1]), (node.path_x[i], node.path_y[i]))
        node = node.parent

import time

def main():
    start_time = time.time()
    screen.fill(white)
    init_obstacles()
    #init_obstacles1()
    #init_case_3_5_split_obstacles()

    initialPoint = None
    goalPoint = None
    currentState = 'init'
    nodes = []
    path_found = False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE):
                sys.exit("Exiting")

            if e.type == pygame.MOUSEBUTTONDOWN:
                if currentState == 'init':
                    if initialPoint is None:
                        if not collides(e.pos):
                            initialPoint = Node(e.pos[0], e.pos[1], yaw=np.deg2rad(0.0))
                            nodes.append(initialPoint)
                            pygame.draw.circle(screen, red, (initialPoint.x, initialPoint.y), GOAL_RADIUS)
                    elif goalPoint is None:
                        if not collides(e.pos):
                            goalPoint = Node(e.pos[0], e.pos[1], yaw=np.deg2rad(90.0))
                            pygame.draw.circle(screen, green, (goalPoint.x, goalPoint.y), GOAL_RADIUS)
                            currentState = 'buildTree'
                else:
                    currentState = 'init'
                    initialPoint = None
                    goalPoint = None
                    nodes.clear()
                    screen.fill(white)
                    init_obstacles()

        if currentState == 'buildTree' and len(nodes) > 0 and goalPoint is not None and not path_found:
            if len(nodes) > NUMNODES:
                print("❌ Reached max nodes without finding goal")
                currentState = 'done'
            else:
                rand_node = get_random_clear()
                nearest = min(nodes, key=lambda n: dist((n.x, n.y), (rand_node.x, rand_node.y)))
                new_node = dubins_steer(nearest, rand_node)
                if new_node:
                    nodes.append(new_node)
                    for i in range(1, len(new_node.path_x)):
                        pygame.draw.line(screen, cyan, (new_node.path_x[i - 1], new_node.path_y[i - 1]), (new_node.path_x[i], new_node.path_y[i]))
                    if dist((new_node.x, new_node.y), (goalPoint.x, goalPoint.y)) < GOAL_RADIUS:
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        print("✅ Goal reached")
                        print(f"⏱ Time taken: {elapsed_time:.4f} seconds")
                        print(f"📏 Path distance: {new_node.cost:.2f} units")
                        print(f"🌲 Tree depth (nodes): {len(nodes)}")
                        print(f"🔁 Number of turns: {len(new_node.path_yaw)}")
                        goalPoint.parent = new_node
                        path_found = True
                        draw_path(goalPoint)

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
