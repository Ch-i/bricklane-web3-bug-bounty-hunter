from manim import *


class PatternExplainer(Scene):
    def construct(self):
        self.show_title()
        self.show_core_logic()
        self.show_attack_flow()
        self.show_defense_pattern()
        self.show_summary()

    # ------------------------------------------------------------------
    # 1. TITLE CARD
    # ------------------------------------------------------------------
    def show_title(self):
        title = Text(
            "Oracle Aggregation & Staleness Detection",
            color=YELLOW,
            font_size=40,
        )
        subtitle = Text(
            "web3 infrastructure pattern",
            color=GREY,
            font_size=24,
        )
        subtitle.next_to(title, DOWN, buff=0.4)
        group = VGroup(title, subtitle)

        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(group))

    # ------------------------------------------------------------------
    # 2. CORE LOGIC, STEP BY STEP
    # ------------------------------------------------------------------
    def show_core_logic(self):
        header = Text("How a protocol reads a price", color=BLUE, font_size=34)
        header.to_edge(UP)
        self.play(Write(header))

        # Three boxes: Oracle -> Protocol -> Action
        oracle = self._box("Chainlink\nFeed", BLUE)
        protocol = self._box("Lending\nProtocol", WHITE)
        action = self._box("Liquidate /\nBorrow", WHITE)

        oracle.shift(LEFT * 4.5)
        action.shift(RIGHT * 4.5)

        boxes = VGroup(oracle, protocol, action)

        a1 = Arrow(oracle.get_right(), protocol.get_left(), color=GREY, buff=0.2)
        a2 = Arrow(protocol.get_right(), action.get_left(), color=GREY, buff=0.2)

        self.play(Create(oracle))
        self.play(Create(a1), Create(protocol))
        self.play(Create(a2), Create(action))
        self.wait(1)

        # Show the returned tuple
        code = MathTex(
            r"(\text{roundId},\ \text{answer},\ \text{updatedAt},\ \text{answeredInRound})",
            font_size=30,
            color=WHITE,
        )
        code.next_to(boxes, DOWN, buff=1.2)
        self.play(Write(code))
        self.wait(1)

        note = Text(
            "Most code keeps only `answer` and ignores the rest",
            color=GREY,
            font_size=24,
        )
        note.next_to(code, DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(2)

        self.core_group = VGroup(boxes, a1, a2, code, note)
        self.play(FadeOut(self.core_group), FadeOut(header))

    # ------------------------------------------------------------------
    # 3. ATTACK / VULNERABILITY FLOW (RED)
    # ------------------------------------------------------------------
    def show_attack_flow(self):
        header = Text("The stale-price failure", color=RED, font_size=34)
        header.to_edge(UP)
        self.play(Write(header))

        vuln = Rectangle(width=10, height=1.2, color=RED)
        vuln_code = MathTex(
            r"(,\ \text{answer},\ ,\ ) = \text{feed.latestRoundData()}",
            font_size=30,
            color=RED,
        )
        vuln_code.move_to(vuln.get_center())
        vuln_block = VGroup(vuln, vuln_code).shift(UP * 1.2)

        self.play(Create(vuln), Write(vuln_code))
        self.play(Indicate(vuln_block, color=RED))
        self.wait(1)

        # The attack steps
        steps = VGroup(
            self._bullet("1. Feed freezes — `updatedAt` never re-checked", RED),
            self._bullet("2. Real market price moves far away", RED),
            self._bullet("3. Protocol values collateral at the OLD price", RED),
            self._bullet("4. Attacker borrows / liquidates the gap", RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        steps.next_to(vuln_block, DOWN, buff=0.8)

        for s in steps:
            self.play(FadeIn(s, shift=RIGHT * 0.3))
            self.wait(0.4)

        self.wait(1)
        loss = Text("Result: protocol drained at a price that isn't real",
                    color=RED, font_size=26)
        loss.next_to(steps, DOWN, buff=0.6)
        self.play(Write(loss))
        self.wait(2)

        self.attack_group = VGroup(vuln_block, steps, loss)
        self.play(FadeOut(self.attack_group), FadeOut(header))

    # ------------------------------------------------------------------
    # 4. DEFENSE PATTERN (GREEN)
    # ------------------------------------------------------------------
    def show_defense_pattern(self):
        header = Text("The defense: validate freshness", color=GREEN, font_size=34)
        header.to_edge(UP)
        self.play(Write(header))

        checks = VGroup(
            self._check(r"\text{require(answer > 0)}"),
            self._check(r"\text{require(updatedAt + maxStaleness} \geq \text{block.timestamp)}"),
            self._check(r"\text{require(answeredInRound} \geq \text{roundId)}"),
            self._check(r"\text{require(sequencerUp \&\& gracePeriodPassed)}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        checks.shift(UP * 0.3)

        for c in checks:
            self.play(FadeIn(c, shift=RIGHT * 0.3))
            self.play(Indicate(c, color=GREEN))
            self.wait(0.3)

        self.wait(1)
        extra = Text(
            "Per-feed maxStaleness + aggregate multiple sources",
            color=GREEN,
            font_size=24,
        )
        extra.next_to(checks, DOWN, buff=0.7)
        self.play(FadeIn(extra))
        self.wait(2)

        self.defense_group = VGroup(checks, extra)
        self.play(FadeOut(self.defense_group), FadeOut(header))

    # ------------------------------------------------------------------
    # 5. SUMMARY / TAKEAWAYS
    # ------------------------------------------------------------------
    def show_summary(self):
        title = Text("Key takeaways", color=YELLOW, font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        points = VGroup(
            self._bullet("Never trust `answer` alone — check `updatedAt`", WHITE),
            self._bullet("Use a per-feed heartbeat, not one global threshold", WHITE),
            self._bullet("Honor minAnswer/maxAnswer circuit breakers", WHITE),
            self._bullet("On L2s, check the sequencer-uptime feed", WHITE),
            self._bullet("Aggregate sources; snapshot to break flash-loan reads", WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        points.next_to(title, DOWN, buff=0.8)

        for p in points:
            self.play(FadeIn(p, shift=RIGHT * 0.3))
            self.wait(0.3)

        self.wait(2)

        closing = Text("Stale or manipulable price = bad price",
                       color=YELLOW, font_size=28)
        closing.next_to(points, DOWN, buff=0.7)
        self.play(Write(closing))
        self.wait(2)

        self.play(FadeOut(VGroup(title, points, closing)))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _box(self, label, color):
        rect = RoundedRectangle(
            width=2.4, height=1.4, corner_radius=0.15, color=color
        )
        text = Text(label, color=color, font_size=24)
        text.move_to(rect.get_center())
        return VGroup(rect, text)

    def _bullet(self, label, color):
        dot = Text("•", color=color, font_size=30)
        text = Text(label, color=color, font_size=26)
        text.next_to(dot, RIGHT, buff=0.25)
        return VGroup(dot, text)

    def _check(self, tex):
        mark = Text("✓", color=GREEN, font_size=30)
        body = MathTex(tex, font_size=28, color=GREEN)
        body.next_to(mark, RIGHT, buff=0.3)
        return VGroup(mark, body)