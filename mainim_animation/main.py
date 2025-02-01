from manim import *

class ImprovedWaterFlow(Scene):
    def construct(self):
        # Water background
        water = Rectangle(width=8, height=3, color=BLUE, fill_opacity=0.5)
        water.move_to(DOWN * 1.5)

        # Water wave effect using multiple sine waves [maybe can be faster]
        wave = FunctionGraph(lambda x: 0.2 * np.sin(2 * x), color=BLUE_B)
        wave.move_to(DOWN * 1.5)

        # Buoy (small floating sphere) [???? not rendernig]
        buoy = Dot(radius=0.15, color=RED).move_to(LEFT * 2 + DOWN * 0.5)

        # Anchor line (dashed)
        anchor_line = DashedLine(start=buoy.get_center(), end=buoy.get_center() + DOWN * 0.5, color=WHITE)

        # Velocity vector arrow
        velocity_vector = Arrow(start=buoy.get_center(), end=buoy.get_center() + RIGHT * 0.5, buff=0, color=YELLOW)

        # Velocity label
        velocity_text = DecimalNumber(0, num_decimal_places=2, color=YELLOW).next_to(velocity_vector, UP)
        velocity_label = VGroup(MathTex(r"v="), velocity_text).arrange(RIGHT).next_to(velocity_vector, UP)

        # Water flow arrows
        arrows = VGroup(*[
            Arrow(LEFT * 3 + RIGHT * i, LEFT * 2 + RIGHT * i, buff=0, color=BLUE_B)
            for i in range(-3, 4, 2)
        ])

        # Add elements to scene
        self.add(water, wave, arrows, buoy, anchor_line, velocity_vector, velocity_label)

        # Water wave animation
        wave.add_updater(lambda m, dt: m.shift(RIGHT * 0.2 * dt) if m.get_right()[0] < 4 else m.shift(LEFT * 8))

        # Arrow movement
        for arrow in arrows:
            arrow.add_updater(lambda m, dt: m.shift(RIGHT * 0.2 * dt) if m.get_right()[0] < 4 else m.shift(LEFT * 8))

        # Buoy motion simulation
        def buoy_motion(m, dt):
            displacement = 0.2 * np.sin(self.time * 2)  # Oscillating motion
            m.shift(RIGHT * displacement * dt)
            velocity_vector.put_start_and_end_on(m.get_center(), m.get_center() + RIGHT * 0.5)
            velocity_text.set_value(abs(displacement * 5))  # Scaling for visibility
            velocity_label.next_to(velocity_vector, UP)
            anchor_line.put_start_and_end_on(m.get_center(), m.get_center() + DOWN * 0.5)

        buoy.add_updater(buoy_motion)

        # Play animation [non error play nahi hora so tried vid main ]
        self.wait(5)
