from manim import *


class PatternExplainer(Scene):
    """Animated explainer: Cross-Chain Message Passing (token bridges)."""

    def construct(self):
        self.show_title()
        self.show_core_logic()
        self.show_attack()
        self.show_defense()
        self.show_summary()

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def labeled_box(self, label, color=BLUE, width=3.2, height=1.6, font_size=24):
        box = Rectangle(width=width, height=height, color=color, stroke_width=3)
        text = Text(label, font_size=font_size, color=WHITE, line_spacing=0.8)
        text.set_width(min(text.width, width - 0.4))
        text.move_to(box.get_center())
        return VGroup(box, text)

    def section_header(self, title, color=WHITE):
        header = Text(title, font_size=34, color=color, weight=BOLD)
        header.to_edge(UP, buff=0.5)
        return header

    # ------------------------------------------------------------------ #
    # 1. Title card
    # ------------------------------------------------------------------ #
    def show_title(self):
        title = Text("Cross-Chain Message Passing", font_size=48, color=BLUE, weight=BOLD)
        subtitle = Text("Token Bridges: Lock-Mint / Burn-Mint", font_size=28, color=GREY)
        domain = Text("Domain: Infrastructure", font_size=22, color=YELLOW)

        group = VGroup(title, subtitle, domain).arrange(DOWN, buff=0.5)
        group.move_to(ORIGIN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.play(FadeIn(domain))
        self.wait(1.5)
        self.play(FadeOut(group))

    # ------------------------------------------------------------------ #
    # 2. Core logic, step by step
    # ------------------------------------------------------------------ #
    def show_core_logic(self):
        header = self.section_header("How a Bridge Works", BLUE)
        self.play(Write(header))

        source = self.labeled_box("Source Gateway\nlock / burn", BLUE)
        attest = self.labeled_box("Attestation Layer\nmultisig / proof", YELLOW)
        dest = self.labeled_box("Dest. Handler\nmint / release", GREEN)

        chain = VGroup(source, attest, dest).arrange(RIGHT, buff=1.0)
        chain.move_to(ORIGIN).shift(UP * 0.3)

        arrow1 = Arrow(source.get_right(), attest.get_left(), buff=0.1, color=WHITE)
        arrow2 = Arrow(attest.get_right(), dest.get_left(), buff=0.1, color=WHITE)

        self.play(Create(source))
        self.play(Create(arrow1), Create(attest))
        self.play(Create(arrow2), Create(dest))
        self.wait(0.5)

        invariant = MathTex(
            r"\text{minted}_{dst} \;\leq\; \text{escrowed}_{src}",
            font_size=36,
            color=GREEN,
        )
        invariant.to_edge(DOWN, buff=0.9)
        caption = Text("The bridge invariant: never mint more than was locked",
                       font_size=22, color=GREY)
        caption.next_to(invariant, DOWN, buff=0.3)

        self.play(Write(invariant))
        self.play(FadeIn(caption))
        self.play(Indicate(invariant, color=GREEN))
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(header, chain, arrow1, arrow2, invariant, caption))
        )

    # ------------------------------------------------------------------ #
    # 3. Attack / vulnerability flow
    # ------------------------------------------------------------------ #
    def show_attack(self):
        header = self.section_header("Attack: Unbacked Mint (Qubit-style)", RED)
        self.play(Write(header))

        source = self.labeled_box("Source Gateway\ntoken = 0x000...0", RED)
        dest = self.labeled_box("Dest. Handler\nmints 77,162 qXETH", RED)
        chain = VGroup(source, dest).arrange(RIGHT, buff=2.5)
        chain.move_to(ORIGIN).shift(UP * 0.3)

        bad_arrow = Arrow(source.get_right(), dest.get_left(), buff=0.1, color=RED)

        steps = VGroup(
            Text("1. deposit(token = address(0), amount = huge)", font_size=22, color=RED),
            Text("2. safeTransferFrom on 0x0 is a NO-OP (no revert)", font_size=22, color=RED),
            Text("3. zero locked  ->  unbacked supply minted", font_size=22, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.to_edge(DOWN, buff=0.7)

        self.play(Create(source))
        self.play(Create(bad_arrow), Create(dest))
        self.play(Indicate(source, color=RED, scale_factor=1.1))

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3))
        self.play(Indicate(dest, color=RED, scale_factor=1.15))
        self.wait(1.5)

        self.play(FadeOut(VGroup(header, chain, bad_arrow, steps)))

    # ------------------------------------------------------------------ #
    # 4. Defense pattern
    # ------------------------------------------------------------------ #
    def show_defense(self):
        header = self.section_header("Defense: Bind & Verify", GREEN)
        self.play(Write(header))

        source = self.labeled_box("Source Gateway\nverify real escrow", GREEN)
        attest = self.labeled_box("Attestation\nattest exact amount", YELLOW)
        dest = self.labeled_box("Dest. Handler\nmint <= escrowed", GREEN)
        chain = VGroup(source, attest, dest).arrange(RIGHT, buff=0.9)
        chain.move_to(ORIGIN).shift(UP * 0.3)

        a1 = Arrow(source.get_right(), attest.get_left(), buff=0.1, color=GREEN)
        a2 = Arrow(attest.get_right(), dest.get_left(), buff=0.1, color=GREEN)

        checks = VGroup(
            Text("require(token != address(0))", font_size=22, color=GREEN),
            Text("bind credited token to the asset actually transferred", font_size=22, color=GREEN),
            Text("assert balanceAfter - balanceBefore == amount", font_size=22, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        checks.to_edge(DOWN, buff=0.7)

        self.play(Create(source))
        self.play(Create(a1), Create(attest))
        self.play(Create(a2), Create(dest))

        for check in checks:
            self.play(FadeIn(check, shift=RIGHT * 0.3))
        self.play(Indicate(chain, color=GREEN))
        self.wait(1.5)

        self.play(FadeOut(VGroup(header, chain, a1, a2, checks)))

    # ------------------------------------------------------------------ #
    # 5. Summary takeaways
    # ------------------------------------------------------------------ #
    def show_summary(self):
        header = self.section_header("Key Takeaways", YELLOW)
        self.play(Write(header))

        box = RoundedRectangle(
            width=11, height=4.6, corner_radius=0.25, color=YELLOW, stroke_width=3
        )
        box.move_to(ORIGIN).shift(DOWN * 0.2)

        takeaways = VGroup(
            Text("- Invariant: minted_dst <= escrowed_src, exactly once",
                 font_size=24, color=WHITE),
            Text("- Always gate the deposit path against address(0)",
                 font_size=24, color=WHITE),
            Text("- Bind the credited asset to the one truly transferred",
                 font_size=24, color=WHITE),
            Text("- Bridges fail catastrophically: >$2.8B lost since 2021",
                 font_size=24, color=RED),
            Text("- Verify balances, not just signatures",
                 font_size=24, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        takeaways.move_to(box.get_center())

        self.play(Create(box))
        for line in takeaways:
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(2)

        self.play(FadeOut(VGroup(header, box, takeaways)))
        self.wait(0.5)