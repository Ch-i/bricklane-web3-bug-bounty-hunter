from manim import *


class PatternExplainer(Scene):
    def construct(self):
        self.show_title()
        self.show_core_logic()
        self.show_attack_flow()
        self.show_defense()
        self.show_summary()

    # ------------------------------------------------------------------
    # 1. Title card
    # ------------------------------------------------------------------
    def show_title(self):
        title = Text("Flash Loan Mechanics", color=BLUE).scale(1.1)
        subtitle = Text("& Composability", color=WHITE).scale(0.9)
        domain = Text("DeFi  •  Security Pattern", color=GREY).scale(0.5)

        group = VGroup(title, subtitle, domain).arrange(DOWN, buff=0.4)

        box = RoundedRectangle(
            width=group.width + 1.5,
            height=group.height + 1.2,
            corner_radius=0.25,
            color=BLUE,
        )

        self.play(Create(box))
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.play(FadeIn(domain))
        self.wait(2)
        self.play(FadeOut(VGroup(box, group)))

    # ------------------------------------------------------------------
    # 2. Core logic, step by step
    # ------------------------------------------------------------------
    def show_core_logic(self):
        heading = Text("The Core Idea: One Atomic Transaction", color=YELLOW).scale(0.6)
        heading.to_edge(UP)
        self.play(Write(heading))

        steps_text = [
            "1.  Borrow huge capital (no collateral)",
            "2.  Move on-chain state that should be expensive",
            "3.  Read the manipulated state as if it were true",
            "4.  Profit from a downstream action",
            "5.  Repay the loan  —  all in ONE tx",
        ]

        boxes = VGroup()
        for line in steps_text:
            label = Text(line, color=WHITE).scale(0.42)
            rect = Rectangle(
                width=8.5,
                height=0.7,
                color=BLUE,
            )
            label.move_to(rect.get_center())
            boxes.add(VGroup(rect, label))

        boxes.arrange(DOWN, buff=0.25)
        boxes.next_to(heading, DOWN, buff=0.5)

        for item in boxes:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.6)

        note = Text(
            "The asset is never the prize — the borrowed state is.",
            color=GREY,
        ).scale(0.4)
        note.next_to(boxes, DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(2)
        self.play(FadeOut(VGroup(heading, boxes, note)))

    # ------------------------------------------------------------------
    # 3. Attack / vulnerability flow (red)
    # ------------------------------------------------------------------
    def show_attack_flow(self):
        heading = Text("Attack: Oracle Manipulation", color=RED).scale(0.6)
        heading.to_edge(UP)
        self.play(Write(heading))

        def make_node(label, color):
            rect = RoundedRectangle(
                width=2.6, height=1.1, corner_radius=0.15, color=color
            )
            txt = Text(label, color=WHITE).scale(0.36)
            txt.move_to(rect.get_center())
            return VGroup(rect, txt)

        attacker = make_node("Flash Loan\n(huge capital)", RED)
        pool = make_node("AMM Pool\nslot0 / reserves", YELLOW)
        oracle = make_node("Protocol reads\nthe lie", RED)
        action = make_node("Mint / Borrow /\nLiquidate", RED)

        nodes = VGroup(attacker, pool, oracle, action).arrange(RIGHT, buff=0.7)
        nodes.next_to(heading, DOWN, buff=1.2)

        self.play(FadeIn(attacker))
        arrows = VGroup()
        for a, b, txt in [
            (attacker, pool, "push price"),
            (pool, oracle, "distorted"),
            (oracle, action, "settle"),
        ]:
            arrow = Arrow(
                a.get_right(), b.get_left(), color=RED, buff=0.15, stroke_width=4
            )
            caption = Text(txt, color=RED).scale(0.3)
            caption.next_to(arrow, UP, buff=0.1)
            self.play(FadeIn(b), Create(arrow), FadeIn(caption), run_time=0.7)
            arrows.add(arrow, caption)

        for node in [attacker, oracle, action]:
            self.play(Indicate(node, color=RED), run_time=0.5)

        victims = Text(
            "Cream • PancakeBunny • Deus DAO • Inverse • WooFi",
            color=GREY,
        ).scale(0.38)
        victims.next_to(nodes, DOWN, buff=1.0)
        self.play(FadeIn(victims))
        self.wait(2)
        self.play(FadeOut(VGroup(heading, nodes, arrows, victims)))

    # ------------------------------------------------------------------
    # 4. Defense pattern (green)
    # ------------------------------------------------------------------
    def show_defense(self):
        heading = Text("Defense: Separate Read from Write", color=GREEN).scale(0.6)
        heading.to_edge(UP)
        self.play(Write(heading))

        principle = Text(
            "No quantity that decides real money may be\n"
            "readable AND writable in one atomic context.",
            color=WHITE,
        ).scale(0.45)
        principle.next_to(heading, DOWN, buff=0.5)
        self.play(Write(principle))

        defenses = [
            "Use a robust oracle (Chainlink / off-chain quote)",
            "Time-weight the price (long-window TWAP)",
            "Split read & consequence across blocks / snapshots",
            "Add execution delay to governance actions",
        ]

        boxes = VGroup()
        for line in defenses:
            label = Text(line, color=WHITE).scale(0.4)
            rect = Rectangle(width=8.5, height=0.7, color=GREEN)
            label.move_to(rect.get_center())
            boxes.add(VGroup(rect, label))

        boxes.arrange(DOWN, buff=0.25)
        boxes.next_to(principle, DOWN, buff=0.5)

        for item in boxes:
            self.play(FadeIn(item, shift=LEFT), run_time=0.5)
            self.play(Indicate(item, color=GREEN), run_time=0.4)

        self.wait(2)
        self.play(FadeOut(VGroup(heading, principle, boxes)))

    # ------------------------------------------------------------------
    # 5. Summary / key takeaways
    # ------------------------------------------------------------------
    def show_summary(self):
        heading = Text("Key Takeaways", color=YELLOW).scale(0.7)
        heading.to_edge(UP)
        self.play(Write(heading))

        takeaways = [
            "Flash loans make 'expensive to move' state cheap for one tx.",
            "Three families: oracle manipulation, governance, sandwich.",
            "Never trust a price you can move and read atomically.",
            "Move the source off-chain, time-weight it, or split blocks.",
        ]

        items = VGroup()
        for i, line in enumerate(takeaways):
            bullet = Text("✓", color=GREEN).scale(0.5)
            text = Text(line, color=WHITE).scale(0.42)
            row = VGroup(bullet, text).arrange(RIGHT, buff=0.3)
            items.add(row)

        items.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        items.next_to(heading, DOWN, buff=0.7)

        for row in items:
            self.play(FadeIn(row, shift=UP), run_time=0.6)

        closing = Text(
            "Atomicity is the weapon — break the atomic read.",
            color=BLUE,
        ).scale(0.5)
        closing.next_to(items, DOWN, buff=0.7)
        self.play(Write(closing))
        self.wait(3)
        self.play(FadeOut(VGroup(heading, items, closing)))