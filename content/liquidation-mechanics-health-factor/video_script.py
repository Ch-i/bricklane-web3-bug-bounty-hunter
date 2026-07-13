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
        title = Text("Liquidation Mechanics", color=YELLOW).scale(1.1)
        subtitle = Text("& Health Factor Math", color=WHITE).scale(0.8)
        domain = Text("DeFi Lending — Pattern Explainer", color=GREY).scale(0.45)

        title.shift(UP * 0.7)
        subtitle.next_to(title, DOWN, buff=0.35)
        domain.next_to(subtitle, DOWN, buff=0.6)

        box = RoundedRectangle(
            width=10.5, height=4.0, corner_radius=0.25, color=BLUE
        )

        self.play(Create(box))
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.play(FadeIn(domain))
        self.wait(1.5)
        self.play(
            FadeOut(box),
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(domain),
        )

    # ------------------------------------------------------------------
    # 2. CORE LOGIC, STEP BY STEP
    # ------------------------------------------------------------------
    def show_core_logic(self):
        heading = Text("The Chain of Trust", color=WHITE).scale(0.7).to_edge(UP)
        self.play(Write(heading))

        labels = ["Oracle\nprices\ncollateral", "Health\nFactor\ncheck", "Liquidator\nrepays debt", "Bad debt\nsocialized"]
        colors = [BLUE, BLUE, BLUE, GREY]
        boxes = VGroup()
        texts = VGroup()

        for label, color in zip(labels, colors):
            rect = Rectangle(width=2.6, height=1.6, color=color)
            txt = Text(label, color=WHITE).scale(0.35)
            txt.move_to(rect.get_center())
            grp = VGroup(rect, txt)
            boxes.add(rect)
            texts.add(txt)

        groups = VGroup(*[VGroup(b, t) for b, t in zip(boxes, texts)])
        groups.arrange(RIGHT, buff=0.7).shift(DOWN * 0.3)

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

        for i in range(len(boxes)):
            self.play(Create(boxes[i]), Write(texts[i]), run_time=0.6)
            if i < len(arrows):
                self.play(Create(arrows[i]), run_time=0.4)

        # The health-factor formula
        formula = MathTex(
            r"HF = \frac{\text{Collateral} \times \text{Liq.\ Threshold}}{\text{Debt}}",
            color=YELLOW,
        ).scale(0.8)
        formula.to_edge(DOWN, buff=0.6)
        self.play(Write(formula))
        self.wait(0.5)

        rule = Text("HF < 1  →  position is liquidatable", color=YELLOW).scale(0.45)
        rule.next_to(formula, UP, buff=0.3)
        self.play(FadeIn(rule), Indicate(boxes[1], color=YELLOW))
        self.wait(1.5)

        self.play(
            FadeOut(heading),
            FadeOut(groups),
            FadeOut(arrows),
            FadeOut(formula),
            FadeOut(rule),
        )

    # ------------------------------------------------------------------
    # 3. ATTACK / VULNERABILITY FLOW  (red)
    # ------------------------------------------------------------------
    def show_attack_flow(self):
        heading = Text("Attack: Oracle Re-Pricing", color=RED).scale(0.7).to_edge(UP)
        self.play(Write(heading))

        steps = [
            "1. Thin / DEX-priced collateral feeds the oracle",
            "2. Flash-loan swap pumps the collateral price",
            "3. Inflated HF lets attacker over-borrow",
            "4. Price reverts — debt > collateral = BAD DEBT",
        ]

        rows = VGroup()
        for s in steps:
            rect = Rectangle(width=10.0, height=0.9, color=RED)
            txt = Text(s, color=WHITE).scale(0.4)
            txt.move_to(rect.get_center())
            rows.add(VGroup(rect, txt))

        rows.arrange(DOWN, buff=0.3).shift(DOWN * 0.2)

        for row in rows:
            self.play(Create(row[0]), Write(row[1]), run_time=0.7)

        warn = Text("$130M+ drained across Cream, Mango, UwuLend ...", color=RED).scale(0.4)
        warn.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(warn))
        for row in rows:
            self.play(Indicate(row[0], color=RED, scale_factor=1.05), run_time=0.25)
        self.wait(1.2)

        self.play(FadeOut(heading), FadeOut(rows), FadeOut(warn))

    # ------------------------------------------------------------------
    # 4. DEFENSE PATTERN  (green)
    # ------------------------------------------------------------------
    def show_defense(self):
        heading = Text("Defense: Robust Pricing & Buffers", color=GREEN).scale(0.65).to_edge(UP)
        self.play(Write(heading))

        defenses = [
            "Manipulation-resistant oracles (TWAP + multi-source)",
            "Sanity caps & deviation bounds on every feed",
            "Conservative liq. thresholds + liquidation bonus",
            "Per-asset supply/borrow caps; isolate thin collateral",
            "Insurance fund / stability pool to absorb shortfall",
        ]

        rows = VGroup()
        for d in defenses:
            rect = RoundedRectangle(
                width=10.2, height=0.78, corner_radius=0.12, color=GREEN
            )
            txt = Text(d, color=WHITE).scale(0.38)
            txt.move_to(rect.get_center())
            rows.add(VGroup(rect, txt))

        rows.arrange(DOWN, buff=0.25).shift(DOWN * 0.1)

        for row in rows:
            self.play(Create(row[0]), Write(row[1]), run_time=0.55)

        check = Text("HF stays honest  ✓  liquidators act in time", color=GREEN).scale(0.45)
        check.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(check))
        self.play(Indicate(rows, color=GREEN, scale_factor=1.03))
        self.wait(1.2)

        self.play(FadeOut(heading), FadeOut(rows), FadeOut(check))

    # ------------------------------------------------------------------
    # 5. SUMMARY / KEY TAKEAWAYS
    # ------------------------------------------------------------------
    def show_summary(self):
        title = Text("Key Takeaways", color=YELLOW).scale(0.8).to_edge(UP)
        self.play(Write(title))

        takeaways = [
            "Bad debt is the failure state of every lending loop.",
            "It accrues from: wrong oracle, instant self-underwatering,",
            "too-small bonus, or a blocked liquidator transaction.",
            "Most lending hacks reduce to mis-priced collateral.",
            "Audit the price path as hard as the liquidation math.",
        ]

        lines = VGroup()
        for t in takeaways:
            lines.add(Text(t, color=WHITE).scale(0.42))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(DOWN * 0.2)

        for line in lines:
            self.play(FadeIn(line), run_time=0.5)

        box = RoundedRectangle(
            width=11.5, height=4.2, corner_radius=0.2, color=YELLOW
        ).move_to(lines.get_center())
        self.play(Create(box))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(lines), FadeOut(box))
        self.wait(0.5)