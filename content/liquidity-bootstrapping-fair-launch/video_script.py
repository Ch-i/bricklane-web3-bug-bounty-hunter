from manim import *


class PatternExplainer(Scene):
    def construct(self):
        self.show_title()
        self.show_core_logic()
        self.show_attack_flow()
        self.show_defense()
        self.show_summary()

    # ------------------------------------------------------------------
    # 1. TITLE CARD
    # ------------------------------------------------------------------
    def show_title(self):
        title = Text("Liquidity Bootstrapping", color=BLUE, weight=BOLD).scale(0.9)
        subtitle = Text("& Fair Launch", color=WHITE).scale(0.7)
        tag = Text("web3 logic pattern  •  economics", color=GREY).scale(0.4)

        subtitle.next_to(title, DOWN, buff=0.3)
        tag.next_to(subtitle, DOWN, buff=0.5)

        box = RoundedRectangle(
            corner_radius=0.2, width=9.5, height=3.5, color=BLUE
        )

        self.play(Create(box))
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.play(FadeIn(tag))
        self.wait(2)
        self.play(
            FadeOut(box),
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(tag),
        )
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 2. CORE LOGIC: the launch state machine
    # ------------------------------------------------------------------
    def show_core_logic(self):
        heading = Text("The Launch State Machine", color=WHITE).scale(0.7)
        heading.to_edge(UP, buff=0.6)
        self.play(Write(heading))

        labels = ["SELLING", "GRADUATING", "FINALIZING", "TRANSFERS ON"]
        colors = [BLUE, YELLOW, YELLOW, GREEN]

        boxes = VGroup()
        texts = VGroup()
        for label, col in zip(labels, colors):
            rect = Rectangle(width=2.6, height=1.1, color=col)
            txt = Text(label, color=col).scale(0.4)
            txt.move_to(rect.get_center())
            boxes.add(rect)
            texts.add(txt)

        boxes.arrange(RIGHT, buff=0.7)
        boxes.move_to(ORIGIN)
        for rect, txt in zip(boxes, texts):
            txt.move_to(rect.get_center())

        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arr = Arrow(
                boxes[i].get_right(),
                boxes[i + 1].get_left(),
                buff=0.1,
                color=WHITE,
                stroke_width=4,
            )
            arrows.add(arr)

        note = Text(
            'The "genesis" path runs once — yet value is densest here.',
            color=GREY,
        ).scale(0.4)
        note.to_edge(DOWN, buff=0.8)

        for i in range(len(boxes)):
            self.play(Create(boxes[i]), Write(texts[i]), run_time=0.5)
            if i < len(arrows):
                self.play(Create(arrows[i]), run_time=0.3)

        self.play(FadeIn(note))
        self.wait(2)

        self.core_group = VGroup(boxes, texts, arrows)
        self.play(FadeOut(note), FadeOut(heading))
        self.wait(0.2)

    # ------------------------------------------------------------------
    # 3. ATTACK FLOW (red)
    # ------------------------------------------------------------------
    def show_attack_flow(self):
        self.play(self.core_group.animate.scale(0.8).to_edge(UP, buff=1.2))

        heading = Text("Attack: Pre-empt the Graduation", color=RED).scale(0.6)
        heading.to_edge(UP, buff=0.4)
        self.play(Write(heading))

        steps = [
            "1. Attacker buys curve tokens early",
            "2. Creates the DEX pair FIRST — skewed",
            "   reserves:  1e10 base  :  1 wei token",
            "3. Launchpad graduates into the bad pool",
            "   amountB = amountA * reserveB / reserveA",
            "4. Attacker swaps out, drains the pool",
        ]

        lines = VGroup(*[Text(s, color=RED).scale(0.42) for s in steps])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        lines.move_to(DOWN * 0.6)

        danger = Rectangle(
            width=lines.width + 0.8,
            height=lines.height + 0.6,
            color=RED,
        )
        danger.move_to(lines.get_center())

        self.play(Create(danger))
        for line in lines:
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=0.45)

        # flag the graduating box as the danger point
        self.play(Indicate(self.core_group[0][1], color=RED, scale_factor=1.2))
        self.play(Indicate(danger, color=RED))
        self.wait(2)

        self.attack_group = VGroup(heading, lines, danger)
        self.play(FadeOut(self.attack_group), FadeOut(self.core_group))
        self.wait(0.2)

    # ------------------------------------------------------------------
    # 4. DEFENSE (green)
    # ------------------------------------------------------------------
    def show_defense(self):
        heading = Text("Defense: Harden the Genesis Path", color=GREEN).scale(0.6)
        heading.to_edge(UP, buff=0.6)
        self.play(Write(heading))

        defenses = [
            "Gate pair creation behind a 'graduated' flag",
            "Set graduated state BEFORE adding liquidity",
            "Enforce slippage: amountMin > 0, never (0, 0)",
            "Order ops so transfers unlock after finalize",
            "Choose initial price — never read manipulable spot",
        ]

        rows = VGroup()
        for d in defenses:
            check = Text("\u2713", color=GREEN).scale(0.6)
            txt = Text(d, color=WHITE).scale(0.42)
            txt.next_to(check, RIGHT, buff=0.3)
            row = VGroup(check, txt)
            rows.add(row)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.move_to(DOWN * 0.3)

        shield = RoundedRectangle(
            corner_radius=0.2,
            width=rows.width + 1.0,
            height=rows.height + 0.8,
            color=GREEN,
        )
        shield.move_to(rows.get_center())

        self.play(Create(shield))
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.5)

        self.play(Indicate(shield, color=GREEN))
        self.wait(2)

        self.defense_group = VGroup(heading, rows, shield)
        self.play(FadeOut(self.defense_group))
        self.wait(0.2)

    # ------------------------------------------------------------------
    # 5. SUMMARY
    # ------------------------------------------------------------------
    def show_summary(self):
        title = Text("Key Takeaways", color=YELLOW, weight=BOLD).scale(0.7)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title))

        takeaways = [
            "The bootstrap window is where value is densest.",
            "Empty pools & first-mover state are attacker-set.",
            "Graduation handoff is front-runnable by default.",
            "Flash loans game fees within a single block.",
            '"Runs once at genesis" is a red flag, not a pass.',
        ]

        bullets = VGroup()
        for t in takeaways:
            dot = Text("\u2022", color=YELLOW).scale(0.6)
            txt = Text(t, color=WHITE).scale(0.42)
            txt.next_to(dot, RIGHT, buff=0.3)
            bullets.add(VGroup(dot, txt))

        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        bullets.move_to(ORIGIN)

        for b in bullets:
            self.play(FadeIn(b, shift=UP * 0.2), run_time=0.5)

        self.wait(1)

        closing = Text(
            "Read the empty-pool branch, the graduation function,",
            color=GREY,
        ).scale(0.4)
        closing2 = Text(
            "and every place an initial price is read, not chosen.",
            color=GREY,
        ).scale(0.4)
        closing.to_edge(DOWN, buff=1.0)
        closing2.next_to(closing, DOWN, buff=0.15)

        self.play(FadeIn(closing), FadeIn(closing2))
        self.wait(2.5)
        self.play(
            FadeOut(bullets),
            FadeOut(title),
            FadeOut(closing),
            FadeOut(closing2),
        )
        self.wait(0.5)