from manim import *


class PatternExplainer(Scene):
    def construct(self):
        self.title_card()
        self.core_logic()
        self.attack_flow()
        self.defense_pattern()
        self.summary()

    # ------------------------------------------------------------------
    # 1. Title card
    # ------------------------------------------------------------------
    def title_card(self):
        title = Text("ERC-4626 Tokenized Vault Standard", color=BLUE)
        title.scale(0.8)
        subtitle = Text("The First-Depositor Inflation Attack", color=WHITE)
        subtitle.scale(0.5)
        subtitle.next_to(title, DOWN, buff=0.4)

        tag = Text("DeFi  •  Share-Price Rounding Vulnerability", color=GREY)
        tag.scale(0.35)
        tag.next_to(subtitle, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.play(FadeIn(tag))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(tag))

    # ------------------------------------------------------------------
    # 2. Core logic: how shares are priced
    # ------------------------------------------------------------------
    def core_logic(self):
        heading = Text("How a Vault Prices Shares", color=BLUE)
        heading.scale(0.6)
        heading.to_edge(UP)
        self.play(Write(heading))

        formula = MathTex(
            r"\text{shares} = \frac{\text{assets} \times \text{totalSupply}}{\text{totalAssets}}",
            color=WHITE,
        )
        formula.scale(0.9)
        self.play(Write(formula))
        self.wait(1)

        note = Text(
            "Integer division ROUNDS DOWN.",
            color=YELLOW,
        )
        note.scale(0.45)
        note.next_to(formula, DOWN, buff=0.8)
        self.play(FadeIn(note))
        self.play(Indicate(note, color=YELLOW))
        self.wait(1)

        danger = Text(
            "If totalAssets can grow without minting shares,\n"
            "the share price can be inflated at will.",
            color=WHITE,
        )
        danger.scale(0.42)
        danger.next_to(note, DOWN, buff=0.5)
        self.play(FadeIn(danger))
        self.wait(2)

        self.play(
            FadeOut(heading),
            FadeOut(formula),
            FadeOut(note),
            FadeOut(danger),
        )

    # ------------------------------------------------------------------
    # 3. Attack flow (red highlights)
    # ------------------------------------------------------------------
    def attack_flow(self):
        heading = Text("The Attack: First-Depositor Donation", color=RED)
        heading.scale(0.55)
        heading.to_edge(UP)
        self.play(Write(heading))

        steps = [
            "1. Deposit 1 wei  ->  mint 1 share (own 100% of supply)",
            "2. Donate a huge amount of underlying directly to vault",
            "3. totalAssets explodes, totalSupply stays = 1",
            "4. Victim deposit rounds DOWN to 0 shares",
            "5. Attacker redeems 1 share, takes donation + deposit",
        ]

        boxes = VGroup()
        labels = VGroup()
        for i, s in enumerate(steps):
            box = Rectangle(width=10.0, height=0.7, color=RED)
            label = Text(s, color=WHITE)
            label.scale(0.36)
            label.move_to(box.get_center())
            group = VGroup(box, label)
            boxes.add(box)
            labels.add(label)

        rows = VGroup(*[VGroup(boxes[i], labels[i]) for i in range(len(steps))])
        rows.arrange(DOWN, buff=0.25)
        rows.next_to(heading, DOWN, buff=0.5)

        for i in range(len(steps)):
            self.play(Create(boxes[i]), Write(labels[i]), run_time=0.8)
            self.play(Indicate(boxes[i], color=RED), run_time=0.5)

        self.wait(1)

        verdict = Text("Victim gets 0 shares. Funds stolen.", color=RED)
        verdict.scale(0.5)
        verdict.next_to(rows, DOWN, buff=0.4)
        self.play(FadeIn(verdict), Indicate(verdict, color=RED))
        self.wait(2)

        self.play(
            FadeOut(heading),
            FadeOut(rows),
            FadeOut(verdict),
        )

    # ------------------------------------------------------------------
    # 4. Defense pattern (green highlights)
    # ------------------------------------------------------------------
    def defense_pattern(self):
        heading = Text("The Defenses", color=GREEN)
        heading.scale(0.6)
        heading.to_edge(UP)
        self.play(Write(heading))

        defenses = [
            "Mint dead shares to address(0) at deployment",
            "Add virtual shares + virtual assets (OZ ERC4626 offset)",
            "Seed the vault with an initial deposit on launch",
            "Track totalAssets internally, not balanceOf(this)",
            "Enforce a minimum-shares-out / slippage check",
        ]

        boxes = VGroup()
        labels = VGroup()
        for d in defenses:
            box = RoundedRectangle(
                width=10.5, height=0.7, corner_radius=0.15, color=GREEN
            )
            label = Text(d, color=WHITE)
            label.scale(0.36)
            label.move_to(box.get_center())
            boxes.add(box)
            labels.add(label)

        rows = VGroup(*[VGroup(boxes[i], labels[i]) for i in range(len(defenses))])
        rows.arrange(DOWN, buff=0.25)
        rows.next_to(heading, DOWN, buff=0.5)

        check = Text("OK", color=GREEN)
        check.scale(0.4)

        for i in range(len(defenses)):
            self.play(Create(boxes[i]), Write(labels[i]), run_time=0.8)
            self.play(Indicate(boxes[i], color=GREEN), run_time=0.4)

        self.wait(1)

        principle = Text(
            "Goal: totalAssets must only move with totalSupply.",
            color=GREEN,
        )
        principle.scale(0.42)
        principle.next_to(rows, DOWN, buff=0.4)
        self.play(FadeIn(principle))
        self.wait(2)

        self.play(
            FadeOut(heading),
            FadeOut(rows),
            FadeOut(principle),
        )

    # ------------------------------------------------------------------
    # 5. Summary / key takeaways
    # ------------------------------------------------------------------
    def summary(self):
        heading = Text("Key Takeaways", color=YELLOW)
        heading.scale(0.65)
        heading.to_edge(UP)
        self.play(Write(heading))

        takeaways = [
            "Rounding-down on share math is the root cause.",
            "Empty vaults (totalSupply == 0) are the danger zone.",
            "Donations inflate totalAssets without new shares.",
            "Same bug hits cToken / LP / liquid-staking forks.",
            "Virtual offsets + dead shares neutralize it.",
        ]

        items = VGroup()
        for t in takeaways:
            line = Text("- " + t, color=WHITE)
            line.scale(0.42)
            items.add(line)

        items.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        items.next_to(heading, DOWN, buff=0.6)

        for line in items:
            self.play(FadeIn(line), run_time=0.6)

        self.wait(1)

        closing = Text(
            "ERC-4626: never trust a vault with an empty balance.",
            color=BLUE,
        )
        closing.scale(0.45)
        closing.next_to(items, DOWN, buff=0.6)
        self.play(Write(closing))
        self.play(Indicate(closing, color=BLUE))
        self.wait(2)

        self.play(FadeOut(heading), FadeOut(items), FadeOut(closing))
        self.wait(1)