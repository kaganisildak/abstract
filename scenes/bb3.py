from manim import *
import random
import os

ball_count = 3
speed_increase_factor = 1

audio_dir = "/com.docker.devenvironments.code/audio"
sound_files = ["c.wav", "cl.wav", "e.wav", "em.wav", "g.wav"]
sound_paths = [os.path.join(audio_dir, file) for file in sound_files]


class BB3(Scene):
    def construct(self):
        hit_count = 1
        circle_boundary = Circle(radius=3, color=WHITE)  # Boundary of the motion

        # Creating multiple balls placed at the center with random colors
        balls = [Dot(point=circle_boundary.get_center(), 
                     color=random.choice([RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]))
                 for _ in range(ball_count)]


        # Gravity vector acting downwards
        gravity = np.array([0, -0.5, 0], dtype=np.float64)

        # Setting a unique initial velocity for each ball
        for i, ball in enumerate(balls):
            angle = 2 * np.pi * i / ball_count
            ball.velocity = np.array([np.cos(angle)*9, np.sin(angle), 0], dtype=np.float64) * 0.5

        # Adding tracers to each ball
        tracers = [TracedPath(ball.get_center, stroke_color=ball.color, stroke_opacity=[0.6, 0]) for ball in balls]

        # Adding the balls, tracers, and the circle to the scene
        self.add(circle_boundary, *balls, *tracers)

        # Update function for each ball's movement
        def update_ball(ball, dt):
            nonlocal hit_count
            dt = np.float64(dt)

            # Update the position and apply gravity
            ball.shift(ball.velocity * dt)
            ball.velocity += gravity * dt

            # Collision detection and update velocity
            if np.linalg.norm(ball.get_center()) > circle_boundary.radius:
                normal_vector = ball.get_center() / np.linalg.norm(ball.get_center())
                ball.velocity -= 2 * np.dot(ball.velocity, normal_vector) * normal_vector
                ball.velocity *= (1 + speed_increase_factor)
                # Play a random sound on collision
                hit_count +=1
                # if hit_count % 3 == 0:
                #     newball = Dot(point=circle_boundary.get_center(), 
                #      color=random.choice([RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]))
                #     angle = 2 * np.pi * i / hit_count
                #     newball.velocity = np.array([np.cos(angle)*3, np.sin(angle)*2, 0], dtype=np.float64) * 0.5
                #     newball.add_updater(update_ball)
                #     newtracer = TracedPath(newball.get_center, stroke_color=newball.color, stroke_opacity=[0.6, 0])
                #     self.add(newball,newtracer)
                sound_to_play = random.choice(sound_paths)
                self.add_sound(sound_to_play, gain=10)

        # Adding the updater to each ball
        for ball in balls:
            ball.add_updater(update_ball)

        # Running the simulation for a specified time
        self.wait(10)
       
        # Removing updaters at the end
        for ball in balls:
            ball.remove_updater(update_ball)
        for ball in balls:
            ball.set_opacity(0)
        circle_boundary.set_opacity(0)
        self.wait(3)