from collections import namedtuple
from math import cos, sin, pi, atan2
import random
import perlin_noise
import sys, pygame
from pygame.locals import *

Point = namedtuple('Point', ('x', 'y'))
Line = namedtuple('Line', ('p1', 'p2'))
Segment = namedtuple('Segment', ('size', 'angle'))
magn = lambda line: ((line.p2.x-line.p1.x)**2 + (line.p2.y-line.p1.y)**2)**.5
width = 1000
height = 500
scale = 75
shiftx = 300
shifty = 400
screen_color = (10, 10, 10)
line_color = (255, 255, 255)

def render(lines):
    screen=pygame.display.set_mode((width,height))
    screen.fill(screen_color)
    for line in lines:
        pygame.draw.line(screen,line_color, 
                         (line.p1.x*scale+shiftx, line.p1.y*scale+shifty), 
                         (line.p2.x*scale+shiftx, line.p2.y*scale+shifty))
    pygame.display.flip()

    while True:
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)

def midpoint(pt1: Point, pt2: Point):
    mid = lambda x1,x2: x1+(x2-x1)/2
    return Point(mid(pt1.x, pt2.x), mid(pt1.y, pt2.y))

def perturb(pt: Point, mag=.01):
    return Point(pt.x+mag*(random.random()-.5), pt.y+mag*(random.random()-.5))
                
def midpoint_disp(lines, mag):
    new_lines = []
    for line in lines:
        mid_point = midpoint(line.p1, line.p2)
        disp_mid = perturb(mid_point, mag)
        new_lines.append(Line(line.p1, disp_mid))
        new_lines.append(Line(disp_mid, line.p2))
    return new_lines

def random_rotate(lines):
    angle = random.random()
    rot = lambda pt, angle: Point(pt.x*cos(angle)-pt.y*sin(angle), pt.x*sin(angle)+pt.y*cos(angle))
    new_lines = []
    for line in lines:
        new_lines.append(Line(rot(line.p1, angle), rot(line.p2, angle)))
    return new_lines

def perlinize(lines):
    pnoisify = lambda pt: Point(pt.x, abs(pt.y+pnoise(pt.x)))
    new_lines = []
    for line in lines:
        new_lines.append(Line(pnoisify(line.p1), pnoisify(line.p2)))
    return new_lines


pnoise = perlin_noise.PerlinNoise(2)

def landmass():
    lines = [Line(Point(0,-1), Point(-1,0)),
              Line(Point(-1,0), Point(0,1)),
              Line(Point(0,1), Point(1,0)),
              Line(Point(1,0), Point(0,-1)),
    ]
    n_iter = 5
    mag = 0.5
    for _ in range(n_iter):
        lines = midpoint_disp(lines, mag=mag)
        mag /=2
    lines = random_rotate(lines)
    return lines
            
def noisy_segment(segment):
    return Segment(segment.size+(.1*random.random()*random.choice([1, -1])), 
                   segment.angle+(.3*random.random()*random.choice([1, -1])))

def add_segment(line, segment):      
    segment = noisy_segment(segment)
    current_angle = atan2(line.p2.y-line.p1.y, line.p2.x-line.p1.x)
    return Line(line.p2, Point(line.p2.x+magn(line)*segment.size*cos(segment.angle-current_angle),
                               line.p2.y-magn(line)*segment.size*sin(segment.angle-current_angle)))
 
def add_tree(line, segment1, segment2):
    return [line, add_segment(line, segment1), add_segment(line, segment2)]

def treeize_iteration(line, segment1, segment2, iteration=0, max_iter=5):
    if iteration==max_iter:
        return [line]
    # segment1 = noisy_segment(segment1)
    # segment2 = noisy_segment(segment2)
    new_line1 = add_segment(line, segment1)
    new_line2 = add_segment(line, segment2)
    new_lines = [line]
    # new_lines.append(Line(new_line1.p2, new_line2.p2))
    new_lines.extend(treeize_iteration(new_line1, segment1, segment2, iteration+1, max_iter))
    new_lines.extend(treeize_iteration(new_line2, segment1, segment2, iteration+1, max_iter))
    return new_lines

def tree_fractal(iterations=5):
    start_line = Line(Point(0, 0), Point(0, -1))
    segment1 = Segment(.8, -.7) 
    segment2 = Segment(.8, .7)
    lines = treeize_iteration(start_line, segment1, segment2, max_iter=iterations)
    return lines
        

if __name__ == '__main__':
    # lines = tree_fractal(7)
    lines = landmass()
    render(lines)