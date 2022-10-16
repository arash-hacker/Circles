#!/usr/bin/env python3
import math
import sys
import pyglet
from pyglet import shapes
import random

w = 600

running = True
window = pyglet.window.Window(w, w)
batch = pyglet.graphics.Batch()
big_circle = shapes.Circle(w/2, w/2, w//2, color=(0, 225, 0), batch=batch)
fps_display = pyglet.window.FPSDisplay(window=window)

points = []
circles = []
cc_batch = []
points2 = {}

STEP = 10
is_frame = False
with_dots = False


def dist(x, xx, y, yy):
    return math.sqrt(((x-xx) ** 2)+((y-yy) ** 2))


for x in range(0, w, STEP):
    for y in range(0, w, STEP):
        if(dist(x, w//2, y, w//2) <= w//2):
            points.append([x, y])
            if(with_dots):
                points2[(x, y)] = shapes.Circle(
                    x, y, 6, color=(255, 255, 255), batch=batch)


def update(dt):
    global points, points2, circles, cc_batch, running, STEP, is_frame
    if((not running) or len(points) == 0):
        return
    [x, y] = random.choice(points)
    radius = (w//2)-dist(x, w//2, y, w//2)
    for [xx, yy, rr] in circles:
        if(dist(xx, x, yy, y)-rr < radius):
            radius = abs(dist(x, xx, y, yy)-rr)

    print("x", x, "y", y, "r", radius)
    cc_batch.append(shapes.Circle(
        x, y, radius, segments=20, color=(
            int(random.random()*255),
            int(random.random()*255),
            int(random.random()*255),
        ), batch=batch))
    circles.append([x, y, radius])

    STEPS = int((radius//STEP)+1)*STEP
    for i in range(x-STEPS, x+STEPS, STEP):
        for j in range(y-STEPS, y+STEPS, STEP):
            if([i, j] in points):
                if (dist(i, x, j, y) <= radius):
                    points.remove([i, j])
                    if(with_dots):
                        del points2[(i, j)]
    if(is_frame):
        running = False


@window.event
def on_key_press(symbol, modifiers):
    global running, is_frame
    if symbol == pyglet.window.key.R:
        running = not running
    if symbol == pyglet.window.key.S:
        is_frame = not is_frame
    if symbol == pyglet.window.key.Q:
        window.close()


pyglet.clock.schedule_interval(update, 1/60)


@ window.event
def on_draw():
    window.clear()
    batch.draw()
    fps_display.draw()


pyglet.app.run()
