from manim import *


class PatternExplainer(Scene):
    def construct(self):
        self.title_card()
        self.core_logic()
        self.attack_flow()
        self.defense_pattern()
        self.summary()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def labeled_box(self, label, color=BLUE, width=2.4, height=1.1, font_size=20):
        box = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=height,
            stroke_color=color,
            fill_color=color,
            fill_opacity=0.15,
        )
        text = Text(label, font_size=font_size, color=WHITE, line_spacing=0.8)
        text.move_to(box.get_center())
        return VGroup(box, text)

    def section_heading(self, label, color=WHITE):
        heading = Text(label, font_size=30, color=color)
        heading.to_edge(UP, buff=0.5)
        return heading

    # ------------------------------------------------------------------
    # 1. Title card
    # ------------------------------------------------------------------
    def title_card(self):
        title = Text("Yield Aggregator", font_size=54, color=YELLOW)
        title2 = Text("Composability Patterns", font_size=54, color=YELLOW)
        title2.next_to(title, DOWN, buff=0.3)
        group = VGroup(title, title2).move_to(ORIGIN)

        subtitle = Text("DeFi Security Pattern", font_size=28, color=GREY)
        subtitle.next_to(group, DOWN, buff=0.6)

        self.play(Write(title), Write(title2))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(group), FadeOut(subtitle))

    # ------------------------------------------------------------------
    # 2. Core logic
    # ------------------------------------------------------------------
    def core_logic(self):
        heading = self.section_heading("Core Logic: How a Yield Aggregator Works", WHITE)
        self.play(Write(heading))

        user = self.labeled_box("User\nDeposits Asset", color=BLUE)
        vault = self.labeled_box("Vault\nMints Shares", color=BLUE)
        strat = self.labeled_box("Strategy\nRoutes Capital", color=BLUE)
        ext = self.labeled_box("External\nProtocols", color=BLUE)

        row = VGroup(user, vault, strat, ext).arrange(RIGHT, buff=0.7)
        row.move_to(UP * 1.2)

        self.play(FadeIn(user))
        a1 = Arrow(user.get_right(), vault.get_left(), buff=0.1, color=WHITE)
        self.play(Create(a1), FadeIn(vault))
        a2 = Arrow(vault.get_right(), strat.get_left(), buff=0.1, color=WHITE)
        self.play(Create(a2), FadeIn(strat))
        a3 = Arrow(strat.get_right(), ext.get_left(), buff=0.1, color=WHITE)
        self.play(Create(a3), FadeIn(ext))

        # Harvest / auto-compound loop
        harvest = self.labeled_box("Harvest\nReward Tokens", color=GREEN, width=2.6)
        harvest.next_to(ext, DOWN, buff=1.3)
        compound = self.labeled_box("Auto-Compound\ninto Principal", color=GREEN, width=2.6)
        compound.next_to(harvest, LEFT, buff=1.0)

        a4 = Arrow(ext.get_bottom(), harvest.get_top(), buff=0.1, color=GREEN)
        a5 = Arrow(harvest.get_left(), compound.get_right(), buff=0.1, color=GREEN)
        a6 = Arrow(compound.get_top(), vault.get_bottom(), buff=0.1, color=GREEN)

        self.play(Create(a4), FadeIn(harvest))
        self.play(Create(a5), FadeIn(compound))
        self.play(Create(a6))

        loop_label = Text("compounding loop", font_size=20, color=GREY)
        loop_label.next_to(compound, DOWN, buff=0.3)
        self.play(FadeIn(loop_label))
        self.wait(2)

        everything = VGroup(
            heading, user, vault, strat, ext, a1, a2, a3,
            harvest, compound, a4, a5, a6, loop_label,
        )
        self.play(FadeOut(everything))

    # ------------------------------------------------------------------
    # 3. Attack / vulnerability flow
    # ------------------------------------------------------------------
    def attack_flow(self):
        heading = self.section_heading("Attack: Flash-Loan Share Price Manipulation", RED)
        self.play(Write(heading))

        formula = Text(
            "pricePerShare = totalAssets / totalSupply",
            font_size=30,
            color=WHITE,
        )
        formula.next_to(heading, DOWN, buff=0.7)
        self.play(Write(formula))

        note = Text(
            "totalAssets is read from LIVE, attacker-movable pool state",
            font_size=22,
            color=YELLOW,
        )
        note.next_to(formula, DOWN, buff=0.35)
        self.play(FadeIn(note))
        self.play(Indicate(formula, color=RED))
        self.wait(1.5)
        self.play(FadeOut(formula), FadeOut(note))

        steps = VGroup(
            Text("1. Flash-loan capital, distort the underlying pool", font_size=24, color=RED),
            Text("2. Share price deflated  ->  deposit cheaply", font_size=24, color=RED),
            Text("3. Re-inflate the pool  ->  shares now overvalued", font_size=24, color=RED),
            Text("4. Withdraw  ->  drain honest depositors' value", font_size=24, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        steps.next_to(heading, DOWN, buff=0.9)

        for step in steps:
            self.play(FadeIn(step))
            self.play(Indicate(step, color=YELLOW))

        caption = Text(
            "Harvest, Yearn, Belt  —  all drained this way",
            font_size=24,
            color=RED,
        )
        caption.next_to(steps, DOWN, buff=0.6)
        box = Rectangle(
            width=caption.width + 0.6,
            height=caption.height + 0.4,
            stroke_color=RED,
            fill_color=RED,
            fill_opacity=0.1,
        )
        box.move_to(caption.get_center())
        self.play(Create(box), FadeIn(caption))
        self.wait(2)

        self.play(FadeOut(VGroup(heading, steps, caption, box)))

    # ------------------------------------------------------------------
    # 4. Defense pattern
    # ------------------------------------------------------------------
    def defense_pattern(self):
        heading = self.section_heading("Defense: Manipulation-Resistant Design", GREEN)
        self.play(Write(heading))

        defenses = VGroup(
            Text("Price shares via TWAP / manipulation-resistant oracles", font_size=24, color=GREEN),
            Text("Never value positions off raw spot pool state", font_size=24, color=GREEN),
            Text("Enforce slippage bounds on harvest swaps (amountOutMin > 0)", font_size=24, color=GREEN),
            Text("Whitelist & freeze strategies; no arbitrary delegatecall", font_size=24, color=GREEN),
            Text("Guard / permission harvest to block griefing & MEV", font_size=24, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        defenses.next_to(heading, DOWN, buff=0.8)

        for item in defenses:
            check = Text("v", font_size=24, color=GREEN)
            check.next_to(item, LEFT, buff=0.25)
            self.play(FadeIn(item), FadeIn(check))
            item.add(check)

        self.play(Indicate(defenses, color=WHITE))
        self.wait(2)
        self.play(FadeOut(VGroup(heading, defenses)))

    # ------------------------------------------------------------------
    # 5. Summary
    # ------------------------------------------------------------------
    def summary(self):
        heading = self.section_heading("Key Takeaways", YELLOW)
        self.play(Write(heading))

        takeaways = VGroup(
            Text("Share pricing & harvesting both touch external state", font_size=24, color=WHITE),
            Text("Every composed protocol is a new trust boundary", font_size=24, color=WHITE),
            Text("Flash loans can move that state in ONE transaction", font_size=24, color=WHITE),
            Text("Contagion: you inherit the risk of everything beneath", font_size=24, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        takeaways.next_to(heading, DOWN, buff=0.8)

        for line in takeaways:
            dot = Text("-", font_size=24, color=YELLOW)
            dot.next_to(line, LEFT, buff=0.25)
            self.play(FadeIn(line), FadeIn(dot))

        question = Text(
            '"What external state does this number depend on,\n'
            'and can someone move it in the same transaction?"',
            font_size=26,
            color=YELLOW,
            line_spacing=0.8,
        )
        question.next_to(takeaways, DOWN, buff=0.7)
        qbox = RoundedRectangle(
            corner_radius=0.15,
            width=question.width + 0.7,
            height=question.height + 0.5,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.08,
        )
        qbox.move_to(question.get_center())
        self.play(Create(qbox), Write(question))
        self.wait(3)

        self.play(FadeOut(VGroup(heading, takeaways, question, qbox)))
        self.wait(0.5)