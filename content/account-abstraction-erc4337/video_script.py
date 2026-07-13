from manim import *


class PatternExplainer(Scene):
    def construct(self):
        self.title_card()
        self.core_logic()
        self.attack_flow()
        self.defense_pattern()
        self.takeaways()

    # ------------------------------------------------------------------
    # 1. Title card
    # ------------------------------------------------------------------
    def title_card(self):
        title = Text("Account Abstraction", color=BLUE).scale(1.2)
        subtitle = Text("ERC-4337 — UserOps, Bundlers & Paymasters", color=GREY).scale(0.5)
        subtitle.next_to(title, DOWN, buff=0.4)
        tag = Text("Infrastructure Pattern", color=YELLOW).scale(0.4)
        tag.next_to(subtitle, DOWN, buff=0.3)

        self.play(Write(title))
        self.play(FadeIn(subtitle), FadeIn(tag))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(tag))
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 2. Core logic: the multi-actor pipeline
    # ------------------------------------------------------------------
    def core_logic(self):
        heading = Text("The UserOperation Pipeline", color=WHITE).scale(0.7).to_edge(UP)
        self.play(Write(heading))

        labels = ["User", "Bundler", "EntryPoint", "Smart\nAccount", "Paymaster"]
        colors = [WHITE, BLUE, YELLOW, GREEN, GREY]
        boxes = VGroup()
        for label, color in zip(labels, colors):
            box = Rectangle(width=2.0, height=1.1, color=color)
            txt = Text(label, color=color).scale(0.38)
            txt.move_to(box.get_center())
            boxes.add(VGroup(box, txt))

        boxes.arrange(RIGHT, buff=0.55).scale(0.95)
        boxes.next_to(heading, DOWN, buff=1.0)

        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arrow = Arrow(
                boxes[i].get_right(),
                boxes[i + 1].get_left(),
                buff=0.1,
                color=WHITE,
                stroke_width=3,
            )
            arrows.add(arrow)

        flow = Text(
            "User signs a UserOp; the EntryPoint calls validateUserOp\n"
            "on the account and validatePaymasterUserOp on the paymaster.",
            color=GREY,
        ).scale(0.4)
        flow.next_to(boxes, DOWN, buff=1.0)

        self.play(Create(boxes[0]))
        for i in range(len(boxes) - 1):
            self.play(Create(arrows[i]), Create(boxes[i + 1]), run_time=0.6)
        self.play(FadeIn(flow))
        self.wait(2)

        self.play(
            FadeOut(boxes),
            FadeOut(arrows),
            FadeOut(flow),
            FadeOut(heading),
        )
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 3. Attack flow: cross-EntryPoint / cross-chain replay
    # ------------------------------------------------------------------
    def attack_flow(self):
        heading = Text("Vulnerability: UserOp Replay", color=RED).scale(0.7).to_edge(UP)
        self.play(Write(heading))

        bug = Text(
            "A custom account rolls its own userOpHash\n"
            "and forgets to bind it to the EntryPoint + chainId.",
            color=WHITE,
        ).scale(0.45)
        bug.next_to(heading, DOWN, buff=0.6)
        self.play(FadeIn(bug))

        hash_box = RoundedRectangle(width=8.0, height=1.0, corner_radius=0.15, color=RED)
        hash_eq = MathTex(
            r"\text{hash} = H(\text{fields},\ \text{chainId},\ \text{address(this)})",
            color=RED,
        ).scale(0.7)
        hash_eq.move_to(hash_box.get_center())
        hash_group = VGroup(hash_box, hash_eq)
        hash_group.next_to(bug, DOWN, buff=0.7)
        self.play(Create(hash_box), Write(hash_eq))
        self.play(Indicate(hash_group, color=RED, scale_factor=1.1))

        missing = Text("Missing: the EntryPoint address!", color=RED).scale(0.5)
        missing.next_to(hash_group, DOWN, buff=0.6)
        self.play(Write(missing))

        ep1 = Rectangle(width=2.6, height=1.0, color=RED)
        ep1_t = Text("EntryPoint A", color=RED).scale(0.35).move_to(ep1.get_center())
        ep2 = Rectangle(width=2.6, height=1.0, color=RED)
        ep2_t = Text("EntryPoint B", color=RED).scale(0.35).move_to(ep2.get_center())
        g1 = VGroup(ep1, ep1_t)
        g2 = VGroup(ep2, ep2_t)
        pair = VGroup(g1, g2).arrange(RIGHT, buff=2.0)
        pair.next_to(missing, DOWN, buff=0.6)
        replay = Arrow(g1.get_right(), g2.get_left(), color=RED, stroke_width=4)
        replay_t = Text("same signature replayed", color=RED).scale(0.3)
        replay_t.next_to(replay, UP, buff=0.1)

        self.play(Create(g1), Create(g2))
        self.play(Create(replay), FadeIn(replay_t))
        self.play(Indicate(g2, color=RED))
        self.wait(2)

        self.play(
            FadeOut(heading), FadeOut(bug), FadeOut(hash_group),
            FadeOut(missing), FadeOut(pair), FadeOut(replay), FadeOut(replay_t),
        )
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 4. Defense pattern
    # ------------------------------------------------------------------
    def defense_pattern(self):
        heading = Text("Defense: Bind the Hash", color=GREEN).scale(0.7).to_edge(UP)
        self.play(Write(heading))

        fix = Text(
            "Bind userOpHash to chainId AND the EntryPoint address,\n"
            "and always enforce the nonce inside validateUserOp.",
            color=WHITE,
        ).scale(0.45)
        fix.next_to(heading, DOWN, buff=0.6)
        self.play(FadeIn(fix))

        good_box = RoundedRectangle(width=9.5, height=1.0, corner_radius=0.15, color=GREEN)
        good_eq = MathTex(
            r"\text{hash} = H(\text{fields},\ \text{chainId},\ \text{entryPoint},\ \text{nonce})",
            color=GREEN,
        ).scale(0.65)
        good_eq.move_to(good_box.get_center())
        good_group = VGroup(good_box, good_eq)
        good_group.next_to(fix, DOWN, buff=0.7)
        self.play(Create(good_box), Write(good_eq))
        self.play(Indicate(good_group, color=GREEN, scale_factor=1.08))

        checks = VGroup(
            Text("✓ Replay across EntryPoints blocked", color=GREEN).scale(0.42),
            Text("✓ Cross-chain replay blocked", color=GREEN).scale(0.42),
            Text("✓ Use ERC-1271, never raw ecrecover", color=GREEN).scale(0.42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        checks.next_to(good_group, DOWN, buff=0.7)
        for c in checks:
            self.play(FadeIn(c), run_time=0.5)
        self.wait(2)

        self.play(
            FadeOut(heading), FadeOut(fix), FadeOut(good_group), FadeOut(checks),
        )
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 5. Takeaways
    # ------------------------------------------------------------------
    def takeaways(self):
        heading = Text("Key Takeaways", color=BLUE).scale(0.8).to_edge(UP)
        self.play(Write(heading))

        points = [
            "AA moves trust to a pipeline: user → bundler → EntryPoint → account → paymaster.",
            "Bind userOpHash to chainId + EntryPoint to stop replay.",
            "Don't assume the EntryPoint checks your account's nonce — enforce it.",
            "After EIP-7702, tx.origin and code.length no longer prove an EOA.",
            "Paymaster mispricing or a missing withdrawTo can drain or trap stake.",
        ]
        items = VGroup()
        for p in points:
            bullet = Text("•  " + p, color=WHITE).scale(0.4)
            items.add(bullet)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        items.next_to(heading, DOWN, buff=0.8)

        for item in items:
            self.play(FadeIn(item), run_time=0.5)
        self.wait(2)

        box = RoundedRectangle(
            width=items.width + 0.8,
            height=items.height + 0.6,
            corner_radius=0.2,
            color=BLUE,
        )
        box.move_to(items.get_center())
        self.play(Create(box))
        self.play(Indicate(box, color=BLUE, scale_factor=1.03))
        self.wait(2)

        self.play(FadeOut(heading), FadeOut(items), FadeOut(box))
        self.wait(0.5)