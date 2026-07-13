from manim import *


class PatternExplainer(Scene):
    def construct(self):
        # ----------------------------------------------------------------
        # 1. TITLE CARD
        # ----------------------------------------------------------------
        title = Text("Auction Mechanisms", color=BLUE, weight=BOLD).scale(1.1)
        subtitle = Text(
            "Dutch  •  English  •  Sealed-Bid",
            color=WHITE,
        ).scale(0.55)
        subtitle.next_to(title, DOWN, buff=0.4)
        domain = Text("web3 logic pattern — economics", color=GREY).scale(0.4)
        domain.next_to(subtitle, DOWN, buff=0.3)

        self.play(Write(title))
        self.play(FadeIn(subtitle), FadeIn(domain))
        self.wait(1.5)
        self.play(FadeOut(subtitle), FadeOut(domain), title.animate.scale(0.5).to_edge(UP))
        self.wait(0.5)

        # ----------------------------------------------------------------
        # 2. CORE LOGIC — the price-discovery state machine
        # ----------------------------------------------------------------
        core_header = Text("Core Logic: a price-discovery state machine", color=YELLOW).scale(0.55)
        core_header.next_to(title, DOWN, buff=0.5)
        self.play(Write(core_header))

        def make_box(label_text, color=WHITE):
            box = RoundedRectangle(corner_radius=0.15, width=3.0, height=1.0, color=color)
            label = Text(label_text, color=color).scale(0.4)
            label.move_to(box.get_center())
            return VGroup(box, label)

        b_start = make_box("Start\n(price curve)", BLUE)
        b_bid = make_box("Bid +\nSettle", BLUE)
        b_finalize = make_box("Finalize\n(deliver asset)", BLUE)

        b_start.move_to(LEFT * 4.5 + DOWN * 0.5)
        b_bid.move_to(DOWN * 0.5)
        b_finalize.move_to(RIGHT * 4.5 + DOWN * 0.5)

        a1 = Arrow(b_start.get_right(), b_bid.get_left(), color=WHITE, buff=0.15)
        a2 = Arrow(b_bid.get_right(), b_finalize.get_left(), color=WHITE, buff=0.15)

        self.play(Create(b_start))
        self.play(Create(a1), Create(b_bid))
        self.play(Create(a2), Create(b_finalize))
        self.wait(0.5)

        # The three fragile ingredients
        ingredients = VGroup(
            Text("1. time-dependent price curve", color=WHITE).scale(0.4),
            Text("2. bid-settlement accounting", color=WHITE).scale(0.4),
            Text("3. adversarial, observable mempool", color=WHITE).scale(0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        ingredients.next_to(b_bid, DOWN, buff=1.0)
        self.play(FadeIn(ingredients))
        self.wait(1.5)

        self.play(
            FadeOut(ingredients),
            FadeOut(a1),
            FadeOut(a2),
            FadeOut(b_start),
            FadeOut(b_finalize),
            FadeOut(core_header),
        )

        # ----------------------------------------------------------------
        # 3. ATTACK / VULNERABILITY FLOW (red)
        # ----------------------------------------------------------------
        attack_header = Text("Vulnerability: rounding leaks value from the bidder", color=RED).scale(0.5)
        attack_header.next_to(title, DOWN, buff=0.5)
        self.play(self.swap(b_bid, RED), Write(attack_header))

        # Show the broken division-before-multiplication math
        bad_math = MathTex(
            r"\text{claim} = \frac{\text{volume}}{\text{price}}",
            color=RED,
        ).scale(0.9)
        bad_math.move_to(UP * 0.8)
        bad_note = Text(
            "integer division rounds the bidder's claim DOWN;\n"
            "seller keeps full payment — remainder is pure loss",
            color=RED,
        ).scale(0.4)
        bad_note.next_to(bad_math, DOWN, buff=0.4)

        self.play(Write(bad_math))
        self.play(FadeIn(bad_note))
        self.play(Indicate(bad_math, color=RED, scale_factor=1.2))
        self.wait(0.5)

        worst = Text(
            "low-decimal token  →  claim rounds to 0  →  100% loss",
            color=RED,
        ).scale(0.42)
        worst.next_to(bad_note, DOWN, buff=0.4)
        self.play(FadeIn(worst))
        self.play(Indicate(worst, color=RED))
        self.wait(1.5)

        self.play(FadeOut(bad_math), FadeOut(bad_note), FadeOut(worst), FadeOut(attack_header))

        # ----------------------------------------------------------------
        # 4. DEFENSE PATTERN (green)
        # ----------------------------------------------------------------
        defense_header = Text("Defense: order operations + guard the lifecycle", color=GREEN).scale(0.5)
        defense_header.next_to(title, DOWN, buff=0.5)
        self.play(self.swap(b_bid, GREEN), Write(defense_header))

        good_math = MathTex(
            r"\text{claim} = \frac{\text{volume} \times \text{base}}{\text{price}}",
            color=GREEN,
        ).scale(0.9)
        good_math.move_to(UP * 0.8)
        good_note = Text("multiply BEFORE divide — preserve precision", color=GREEN).scale(0.42)
        good_note.next_to(good_math, DOWN, buff=0.4)

        self.play(Write(good_math))
        self.play(FadeIn(good_note))
        self.play(Indicate(good_math, color=GREEN, scale_factor=1.2))
        self.wait(0.5)

        defenses = VGroup(
            Text("validate start/end timestamps & price bounds", color=GREEN).scale(0.4),
            Text("atomic finalize: settle + deliver in one step", color=GREEN).scale(0.4),
            Text("recovery path for the no-bids terminal state", color=GREEN).scale(0.4),
            Text("commit-reveal to hide sealed bids on-chain", color=GREEN).scale(0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        defenses.next_to(good_note, DOWN, buff=0.45)

        for d in defenses:
            self.play(FadeIn(d), run_time=0.45)
        self.wait(1.5)

        self.play(
            FadeOut(good_math),
            FadeOut(good_note),
            FadeOut(defenses),
            FadeOut(defense_header),
            FadeOut(b_bid),
        )

        # ----------------------------------------------------------------
        # 5. SUMMARY / KEY TAKEAWAYS
        # ----------------------------------------------------------------
        summary_header = Text("Key Takeaways", color=YELLOW, weight=BOLD).scale(0.7)
        summary_header.next_to(title, DOWN, buff=0.6)
        self.play(Write(summary_header))

        takeaways = VGroup(
            Text("• Bug class is independent of auction flavor", color=WHITE).scale(0.45),
            Text("• Price-curve math: multiply before divide, bound the price", color=WHITE).scale(0.45),
            Text("• Lifecycle integrity: validate & make transitions atomic", color=WHITE).scale(0.45),
            Text("• Mempool is adversarial: orderings are observable", color=WHITE).scale(0.45),
            Text("• Value silently leaks from the party you meant to protect", color=RED).scale(0.45),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        takeaways.next_to(summary_header, DOWN, buff=0.5)

        summary_box = RoundedRectangle(
            corner_radius=0.2,
            width=takeaways.width + 0.8,
            height=takeaways.height + 0.6,
            color=GREY,
        )
        summary_box.move_to(takeaways.get_center())

        self.play(Create(summary_box))
        for t in takeaways:
            self.play(FadeIn(t), run_time=0.5)
        self.wait(2)

        self.play(
            FadeOut(takeaways),
            FadeOut(summary_box),
            FadeOut(summary_header),
            FadeOut(title),
        )
        self.wait(0.5)

    # Helper: recolor a VGroup box+label by transforming into a fresh copy
    def swap(self, group, color):
        box, label = group
        new_box = box.copy().set_color(color)
        new_label = label.copy().set_color(color)
        return AnimationGroup(Transform(box, new_box), Transform(label, new_label))