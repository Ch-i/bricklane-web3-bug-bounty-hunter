from manim import *


class PatternExplainer(Scene):
    def construct(self):
        self.title_card()
        self.core_logic()
        self.attack_flow()
        self.defense_pattern()
        self.summary()

    # ------------------------------------------------------------------ #
    # 1. Title card
    # ------------------------------------------------------------------ #
    def title_card(self):
        title = Text("Concentrated Liquidity", color=BLUE, weight=BOLD).scale(1.1)
        subtitle = Text("Uniswap V3 / V4 Math", color=WHITE).scale(0.7)
        tag = Text("DeFi  ·  Tick & Fee-Growth Pitfalls", color=GREY).scale(0.45)

        group = VGroup(title, subtitle, tag).arrange(DOWN, buff=0.4)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.play(FadeIn(tag))
        self.wait(2)
        self.play(FadeOut(group))

    # ------------------------------------------------------------------ #
    # 2. Core logic — liquidity over a bounded range
    # ------------------------------------------------------------------ #
    def core_logic(self):
        heading = Text("Core Idea: Liquidity in a Price Range", color=BLUE).scale(0.6)
        heading.to_edge(UP)
        self.play(Write(heading))

        # A price axis with a bounded liquidity range [tickLower, tickUpper)
        axis = Rectangle(width=10.0, height=0.12, color=GREY, fill_opacity=1).shift(DOWN * 0.5)

        range_box = Rectangle(width=3.2, height=1.4, color=BLUE, fill_opacity=0.25)
        range_box.move_to(axis.get_center() + UP * 0.7)

        lower = Text("tickLower", color=WHITE).scale(0.38)
        upper = Text("tickUpper", color=WHITE).scale(0.38)
        lower.next_to(range_box, DOWN, buff=0.15).align_to(range_box, LEFT)
        upper.next_to(range_box, DOWN, buff=0.15).align_to(range_box, RIGHT)

        l_label = Text("L = active liquidity", color=BLUE).scale(0.42)
        l_label.move_to(range_box.get_center())

        self.play(Create(axis))
        self.play(Create(range_box), FadeIn(l_label))
        self.play(FadeIn(lower), FadeIn(upper))
        self.wait(1)

        # The current price marker and the three-branch conversion
        price = Arrow(start=UP * 0.4, end=DOWN * 0.4, color=YELLOW, buff=0)
        price.move_to(range_box.get_center() + DOWN * 0.0)
        price.next_to(axis, UP, buff=0).shift(LEFT * 0.4)
        price_lbl = Text("sqrtPriceX96", color=YELLOW).scale(0.38)
        price_lbl.next_to(price, UP, buff=0.1)

        self.play(Create(price), FadeIn(price_lbl))

        branches = VGroup(
            Text("below range  ->  100% token0", color=WHITE).scale(0.42),
            Text("inside range  ->  token0 + token1", color=WHITE).scale(0.42),
            Text("above range  ->  100% token1", color=WHITE).scale(0.42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        branches.to_edge(DOWN, buff=0.5)

        self.play(Write(branches))
        self.wait(1)
        self.play(Indicate(branches[1], color=YELLOW))
        self.wait(1)

        self.play(
            FadeOut(VGroup(heading, axis, range_box, lower, upper,
                           l_label, price, price_lbl, branches))
        )

    # ------------------------------------------------------------------ #
    # 3. Attack / vulnerability flow (red)
    # ------------------------------------------------------------------ #
    def attack_flow(self):
        heading = Text("Vulnerability: Unsafe liquidityNet Cast", color=RED).scale(0.6)
        heading.to_edge(UP)
        self.play(Write(heading))

        # liquidityNet is int128 and can be negative when crossing a tick
        fact = MathTex(r"\text{liquidityNet} : \texttt{int128}", color=WHITE).scale(0.8)
        fact.next_to(heading, DOWN, buff=0.6)
        self.play(Write(fact))

        bad_box = RoundedRectangle(width=7.0, height=1.0, corner_radius=0.15,
                                   color=RED, fill_opacity=0.15)
        bad_box.next_to(fact, DOWN, buff=0.6)
        bad_code = MathTex(r"\texttt{uint128(\_liquidityNet)}", color=RED).scale(0.7)
        bad_code.move_to(bad_box.get_center())
        self.play(Create(bad_box), Write(bad_code))
        self.wait(0.5)

        # The two's-complement blow-up
        arrow = Arrow(start=bad_box.get_bottom(), end=bad_box.get_bottom() + DOWN * 0.9,
                      color=RED, buff=0.1)
        blowup = MathTex(r"-1 \;\longrightarrow\; 2^{128}-1", color=RED).scale(0.8)
        blowup.next_to(arrow, DOWN, buff=0.2)

        self.play(Create(arrow))
        self.play(Write(blowup))
        self.play(Indicate(blowup, color=RED, scale_factor=1.3))

        consequence = Text("active liquidity silently inflated  ->  drain pool",
                           color=RED).scale(0.45)
        consequence.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(consequence, shift=UP * 0.3))
        self.wait(1.5)

        self.play(FadeOut(VGroup(heading, fact, bad_box, bad_code,
                                 arrow, blowup, consequence)))

    # ------------------------------------------------------------------ #
    # 4. Defense pattern (green)
    # ------------------------------------------------------------------ #
    def defense_pattern(self):
        heading = Text("Defense: Use Canonical Libraries", color=GREEN).scale(0.6)
        heading.to_edge(UP)
        self.play(Write(heading))

        good_box = RoundedRectangle(width=8.0, height=1.0, corner_radius=0.15,
                                    color=GREEN, fill_opacity=0.15)
        good_box.next_to(heading, DOWN, buff=0.7)
        good_code = MathTex(r"\texttt{LiquidityMath.addDelta(L, liquidityNet)}",
                            color=GREEN).scale(0.6)
        good_code.move_to(good_box.get_center())
        self.play(Create(good_box), Write(good_code))
        self.wait(0.5)

        checks = VGroup(
            Text("handles signed int128 deltas safely", color=GREEN).scale(0.42),
            Text("round ticks toward -inf, not toward zero", color=GREEN).scale(0.42),
            Text("fee growth: keep subtraction in unchecked{}", color=GREEN).scale(0.42),
            Text("read per-position state, never slot0 spot", color=GREEN).scale(0.42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        checks.next_to(good_box, DOWN, buff=0.6)

        for line in checks:
            check = Text("OK", color=GREEN).scale(0.4)
            check.next_to(line, LEFT, buff=0.25)
            self.play(FadeIn(check), Write(line), run_time=0.6)
        self.wait(1.5)

        self.play(FadeOut(VGroup(heading, good_box, good_code, checks)),
                  *[FadeOut(m) for m in self.mobjects if m not in
                    [heading, good_box, good_code, checks]])

    # ------------------------------------------------------------------ #
    # 5. Summary of key takeaways
    # ------------------------------------------------------------------ #
    def summary(self):
        heading = Text("Key Takeaways", color=BLUE, weight=BOLD).scale(0.7)
        heading.to_edge(UP, buff=0.8)
        self.play(Write(heading))

        takeaways = VGroup(
            Text("1. Liquidity L lives in [tickLower, tickUpper)", color=WHITE).scale(0.45),
            Text("2. Amounts depend on price vs. range (3 branches)", color=WHITE).scale(0.45),
            Text("3. Never raw-cast signed liquidityNet to uint", color=RED).scale(0.45),
            Text("4. Round ticks with the sign; respect tickSpacing", color=YELLOW).scale(0.45),
            Text("5. Trust audited math libs over re-implementations", color=GREEN).scale(0.45),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        takeaways.next_to(heading, DOWN, buff=0.6)

        box = RoundedRectangle(width=10.0, height=takeaways.height + 0.8,
                               corner_radius=0.2, color=GREY)
        box.move_to(takeaways.get_center())

        self.play(Create(box))
        for line in takeaways:
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(2)

        self.play(FadeOut(VGroup(heading, box, takeaways)))
        self.wait(0.5)