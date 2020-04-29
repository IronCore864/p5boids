from math import atan2, sqrt, pow
from random import random

from p5 import translate, rotate, triangle

from conf import width, height, visual_range, centering_factor, min_distance, avoid_factor, margin, turn_factor, \
    speed_limit, matching_factor


class Boid:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def show(self):
        translate(self.x, self.y)
        angle = atan2(self.dy, self.dx)
        rotate(angle)
        # fixed sized "boid"
        triangle(
            [0, 0],
            [-10, 4],
            [-10, -4],
        )
        rotate(-angle)
        translate(-self.x, -self.y)

    def distance(self, boid):
        return sqrt(
            pow((self.x - boid.x), 2) + pow((self.y - boid.y), 2)
        )

    def fly_towards_center(self, all_boids):
        center_x = 0
        center_y = 0
        num_neighbors = 0
        for b in all_boids:
            if self.distance(b) < visual_range:
                center_x += b.x
                center_y += b.y
                num_neighbors += 1
        if num_neighbors:
            center_x = center_x / num_neighbors
            center_y = center_y / num_neighbors
            self.dx += (center_x - self.x) * centering_factor
            self.dy += (center_y - self.y) * centering_factor

    def keep_within_boundaries(self):
        if self.x < margin:
            self.dx += turn_factor
        if self.x > width - margin:
            self.dx -= turn_factor
        if self.y < margin:
            self.dy += turn_factor
        if self.y > height - margin:
            self.dy -= turn_factor

    def avoid_others(self, boids):
        move_x = 0
        move_y = 0
        for boid in boids:
            if boid != self:
                if self.distance(boid) < min_distance:
                    move_x += self.x - boid.x
                    move_y += self.y - boid.y

        self.dx += move_x * avoid_factor
        self.dy += move_y * avoid_factor

    def limit_speed(self):
        speed = sqrt(pow(self.dx, 2) + pow(self.dy, 2))
        if speed > speed_limit:
            self.dx = (self.dx / speed) * speed_limit
            self.dy = (self.dy / speed) * speed_limit

    def match_velocity(self, boids):
        avg_dx = 0
        avg_dy = 0
        num_neighbours = 0

        for boid in boids:
            if self.distance(boid) < visual_range:
                avg_dx += boid.dx
                avg_dy += boid.dy
                num_neighbours += 1

        if num_neighbours:
            avg_dx = avg_dx / num_neighbours
            avg_dy = avg_dy / num_neighbours

            self.dx += (avg_dx - self.dx) * matching_factor
            self.dy += (avg_dy - self.dy) * matching_factor

    def random_when_alone(self, boids):
        alone = True
        for boid in boids:
            if boid != self:
                if self.distance(boid) > visual_range:
                    continue
                else:
                    alone = False
                    break
        if alone:
            self.dx += random() * 10 - 5
            self.dy += random() * 10 - 5
