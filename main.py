from random import random

from p5 import *

from boid import Boid
from conf import width, height, color, background_color, num_of_boids

boids = [
    Boid(
        random() * width,
        random() * height,
        random() * 10 - 5,
        random() * 10 - 5
    ) for _ in range(num_of_boids)
]


def setup():
    size(width, height)
    no_stroke()
    fill(*color)


def draw():
    background(*background_color)
    for boid in boids:
        boid.random_when_alone(boids)
        boid.fly_towards_center(boids)
        boid.avoid_others(boids)
        boid.match_velocity(boids)
        boid.limit_speed()
        boid.keep_within_boundaries()
        boid.update()
        boid.show()


run()
