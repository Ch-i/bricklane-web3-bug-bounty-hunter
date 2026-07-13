from manim import *


class PatternExplainer(Scene):
    def construct(self):
        self.title_card()
        self.core_logic()
        self.attack_flow()
        self.defense_pattern()
        self.summary()

    # ------------------------------------------------------------------
    # 1. TITLE CARD
    # ------------------------------------------------------------------
    def title_card(self):
        title = Text("Denial of Service", color=WHITE, weight=BOLD).scale(1.3)
        subtitle = Text("& Gas Griefing", color=RED, weight=BOLD).scale(1.1)
        tag = Text("web3 security pattern", color=GREY).scale(0.5)

        title.to_edge(UP, buff=2.0)
        subtitle.next_to(title, DOWN, buff=0.4)
        tag.next_to(subtitle, DOWN, buff=0.6)

        line = Rectangle(width=8.0, height=0.05, color=BLUE,
                         fill_opacity=1).next_to(tag, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.play(FadeIn(tag), Create(line))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, subtitle, tag, line)))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def section_header(self, label, color):
        header = Text(label, color=color, weight=BOLD).scale(0.8)
        header.to_edge(UP, buff=0.5)
        self.play(FadeIn(header, shift=DOWN * 0.3))
        return header

    def make_box(self, label, color, width=3.2, height=1.0):
        box = RoundedRectangle(corner_radius=0.15, width=width, height=height,
                               color=color)
        txt = Text(label, color=WHITE).scale(0.4)
        txt.move_to(box.get_center())
        return VGroup(box, txt)

    # ------------------------------------------------------------------
    # 2. CORE LOGIC
    # ------------------------------------------------------------------
    def core_logic(self):
        header = self.section_header("The Pattern: push-payment loop", BLUE)

        intro = Text(
            "A function loops over a growing list and pushes value to each entry.",
            color=GREY).scale(0.45)
        intro.next_to(header, DOWN, buff=0.5)
        self.play(FadeIn(intro))

        contract = self.make_box("withdrawAll()", BLUE, width=3.6)
        contract.next_to(intro, DOWN, buff=0.7)
        self.play(Create(contract[0]), Write(contract[1]))

        # the list it iterates over
        users = VGroup()
        labels = ["user[0]", "user[1]", "user[2]", "user[n]"]
        for lbl in labels:
            users.add(self.make_box(lbl, WHITE, width=2.2, height=0.7))
        users.arrange(RIGHT, buff=0.4)
        users.next_to(contract, DOWN, buff=1.0)
        self.play(*[Create(u[0]) for u in users],
                  *[Write(u[1]) for u in users])

        loop = MathTex(r"\text{for each } i:\ \ \text{transfer}(user[i])",
                       color=YELLOW).scale(0.7)
        loop.next_to(users, DOWN, buff=0.7)
        self.play(Write(loop))

        # sweep through the loop
        for u in users:
            arrow = Arrow(contract.get_bottom(), u[0].get_top(),
                          color=YELLOW, buff=0.15, stroke_width=3)
            self.play(Create(arrow), Indicate(u, color=YELLOW), run_time=0.4)
            self.play(FadeOut(arrow), run_time=0.2)

        self.wait(1.0)
        self.core_group = VGroup(header, intro, contract, users, loop)
        self.play(FadeOut(self.core_group))

    # ------------------------------------------------------------------
    # 3. ATTACK FLOW
    # ------------------------------------------------------------------
    def attack_flow(self):
        header = self.section_header("The Attack: wedge the whole flow", RED)

        contract = self.make_box("withdrawAll()", BLUE, width=3.6)
        contract.next_to(header, DOWN, buff=0.7)
        self.play(Create(contract[0]), Write(contract[1]))

        good = self.make_box("honest user", GREEN, width=2.4, height=0.8)
        attacker = self.make_box("attacker", RED, width=2.4, height=0.8)
        more = self.make_box("everyone else", GREY, width=2.4, height=0.8)
        row = VGroup(good, attacker, more).arrange(RIGHT, buff=0.5)
        row.next_to(contract, DOWN, buff=1.1)
        self.play(*[Create(b[0]) for b in row], *[Write(b[1]) for b in row])

        # honest transfer succeeds
        a1 = Arrow(contract.get_bottom(), good[0].get_top(),
                   color=GREEN, buff=0.15)
        self.play(Create(a1), Indicate(good, color=GREEN))

        # attacker reverts
        a2 = Arrow(contract.get_bottom(), attacker[0].get_top(),
                   color=RED, buff=0.15)
        revert = Text("revert() / return bomb", color=RED).scale(0.4)
        revert.next_to(attacker, DOWN, buff=0.3)
        self.play(Create(a2))
        self.play(Indicate(attacker, color=RED), Write(revert))

        # the revert bubbles up and bricks the call
        boom = Text("entire transaction reverts", color=RED,
                    weight=BOLD).scale(0.55)
        boom.next_to(row, DOWN, buff=1.0)
        self.play(Transform(revert.copy(), boom),
                  Indicate(contract, color=RED),
                  Indicate(more, color=RED))

        cross = MathTex(r"\Rightarrow\ \text{funds frozen for all}",
                        color=RED).scale(0.7)
        cross.next_to(boom, DOWN, buff=0.4)
        self.play(Write(cross))

        self.wait(1.5)
        self.attack_group = VGroup(header, contract, row, a1, a2,
                                   revert, boom, cross)
        self.play(FadeOut(self.attack_group))

    # ------------------------------------------------------------------
    # 4. DEFENSE PATTERN
    # ------------------------------------------------------------------
    def defense_pattern(self):
        header = self.section_header("The Defense: pull over push", GREEN)

        intro = Text("Let each user withdraw their own funds.",
                     color=GREY).scale(0.45)
        intro.next_to(header, DOWN, buff=0.5)
        self.play(FadeIn(intro))

        ledger = self.make_box("credits[user] += amount", GREEN, width=4.6)
        ledger.next_to(intro, DOWN, buff=0.7)
        self.play(Create(ledger[0]), Write(ledger[1]))

        good = self.make_box("honest user", GREEN, width=2.4, height=0.8)
        attacker = self.make_box("attacker", RED, width=2.4, height=0.8)
        row = VGroup(good, attacker).arrange(RIGHT, buff=1.2)
        row.next_to(ledger, DOWN, buff=1.1)
        self.play(*[Create(b[0]) for b in row], *[Write(b[1]) for b in row])

        a1 = Arrow(good[0].get_top(), ledger.get_bottom(),
                   color=GREEN, buff=0.15)
        ok = Text("withdraw() OK", color=GREEN).scale(0.4)
        ok.next_to(good, DOWN, buff=0.3)
        self.play(Create(a1), Indicate(good, color=GREEN), Write(ok))

        a2 = Arrow(attacker[0].get_top(), ledger.get_bottom(),
                   color=RED, buff=0.15)
        isolated = Text("revert hurts only attacker", color=GREY).scale(0.4)
        isolated.next_to(attacker, DOWN, buff=0.3)
        self.play(Create(a2), Indicate(attacker, color=RED), Write(isolated))

        note = VGroup(
            Text("Other mitigations:", color=WHITE).scale(0.45),
            Text("• cap / paginate unbounded loops", color=GREEN).scale(0.4),
            Text("• gas-limit external calls, ignore returndata", color=GREEN).scale(0.4),
            Text("• avoid strict balance equality checks", color=GREEN).scale(0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        note.next_to(row, DOWN, buff=0.9)
        self.play(FadeIn(note, shift=UP * 0.3))

        self.wait(1.5)
        self.defense_group = VGroup(header, intro, ledger, row, a1, a2,
                                    ok, isolated, note)
        self.play(FadeOut(self.defense_group))

    # ------------------------------------------------------------------
    # 5. SUMMARY
    # ------------------------------------------------------------------
    def summary(self):
        title = Text("Key Takeaways", color=YELLOW, weight=BOLD).scale(0.9)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title))

        points = [
            ("Q", "Can one actor make this uncallable for everyone?", WHITE),
            ("1", "Unbounded loops can exceed the block gas limit", RED),
            ("2", "Pushed transfers let one revert wedge the batch", RED),
            ("3", "Return bombs grief callers via memory expansion", RED),
            ("4", "Prefer pull-payments; cap loops; bound gas", GREEN),
        ]

        rows = VGroup()
        for tag, text, color in points:
            chip = RoundedRectangle(corner_radius=0.1, width=0.7, height=0.7,
                                    color=color)
            chip_txt = Text(tag, color=color).scale(0.5)
            chip_txt.move_to(chip.get_center())
            body = Text(text, color=color).scale(0.45)
            group = VGroup(VGroup(chip, chip_txt), body).arrange(RIGHT, buff=0.4)
            rows.add(group)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        rows.next_to(title, DOWN, buff=0.7)

        for row in rows:
            self.play(Create(row[0][0]), Write(row[0][1]),
                      FadeIn(row[1], shift=RIGHT * 0.3), run_time=0.6)

        self.wait(1.0)
        closing = Text("Cheap to attack, expensive to suffer.",
                       color=YELLOW).scale(0.5)
        closing.next_to(rows, DOWN, buff=0.7)
        self.play(Write(closing))
        self.wait(2.0)
        self.play(FadeOut(VGroup(title, rows, closing)))