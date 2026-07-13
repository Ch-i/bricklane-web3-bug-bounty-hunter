from manim import *


class PatternExplainer(Scene):
    def construct(self):
        self.show_title()
        self.show_core_logic()
        self.show_attack()
        self.show_defense()
        self.show_summary()

    # ------------------------------------------------------------------
    # 1. TITLE CARD
    # ------------------------------------------------------------------
    def show_title(self):
        title = Text("Checks-Effects-Interactions", color=BLUE).scale(0.9)
        subtitle = Text("The reentrancy defense pattern", color=GREY).scale(0.5)
        subtitle.next_to(title, DOWN, buff=0.4)
        domain = Text("security", color=YELLOW).scale(0.4)
        domain.next_to(subtitle, DOWN, buff=0.3)

        box = RoundedRectangle(
            width=title.width + 1.2,
            height=title.height + 2.2,
            corner_radius=0.2,
            color=BLUE,
        )
        box.move_to(title.get_center() + DOWN * 0.55)

        self.play(Create(box))
        self.play(Write(title))
        self.play(FadeIn(subtitle), FadeIn(domain))
        self.wait(2)
        self.play(
            FadeOut(box), FadeOut(title), FadeOut(subtitle), FadeOut(domain)
        )

    # ------------------------------------------------------------------
    # Helper: build a labelled step box
    # ------------------------------------------------------------------
    def make_step(self, label, detail, color):
        rect = Rectangle(width=5.6, height=1.1, color=color)
        name = Text(label, color=color).scale(0.5)
        body = Text(detail, color=WHITE).scale(0.33)
        name.next_to(rect.get_left(), RIGHT, buff=0.3)
        body.next_to(name, DOWN, buff=0.12, aligned_edge=LEFT)
        return VGroup(rect, name, body)

    # ------------------------------------------------------------------
    # 2. CORE LOGIC — THE THREE PHASES
    # ------------------------------------------------------------------
    def show_core_logic(self):
        heading = Text("The three phases of a state-changing call", color=WHITE)
        heading.scale(0.5).to_edge(UP)
        self.play(Write(heading))

        checks = self.make_step(
            "1. CHECKS", "require(balance[msg.sender] >= amount)", YELLOW
        )
        effects = self.make_step(
            "2. EFFECTS", "balance[msg.sender] -= amount", GREEN
        )
        interactions = self.make_step(
            "3. INTERACTIONS", "msg.sender.call{value: amount}(...)", BLUE
        )

        steps = VGroup(checks, effects, interactions).arrange(DOWN, buff=0.45)
        steps.next_to(heading, DOWN, buff=0.6)

        for step in steps:
            self.play(Create(step[0]))
            self.play(Write(step[1]), FadeIn(step[2]))
            self.wait(0.4)

        arrow1 = Arrow(checks.get_bottom(), effects.get_top(), color=GREY, buff=0.1)
        arrow2 = Arrow(
            effects.get_bottom(), interactions.get_top(), color=GREY, buff=0.1
        )
        self.play(Create(arrow1), Create(arrow2))

        note = Text(
            "Validate first, update state, THEN talk to the outside world",
            color=GREY,
        ).scale(0.4)
        note.next_to(steps, DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(2)

        self.core_group = VGroup(heading, steps, arrow1, arrow2, note)
        self.play(FadeOut(self.core_group))

    # ------------------------------------------------------------------
    # 3. ATTACK FLOW — REENTRANCY (interaction BEFORE effect)
    # ------------------------------------------------------------------
    def show_attack(self):
        heading = Text("Vulnerable ordering: Interaction before Effect", color=RED)
        heading.scale(0.5).to_edge(UP)
        self.play(Write(heading))

        check = self.make_step(
            "CHECK", "require(balance[attacker] > 0)", YELLOW
        )
        interact = self.make_step(
            "INTERACT", "attacker.call{value: bal}('')   <-- too early!", RED
        )
        effect = self.make_step(
            "EFFECT", "balance[attacker] = 0   <-- never reached", GREY
        )

        steps = VGroup(check, interact, effect).arrange(DOWN, buff=0.5)
        steps.next_to(heading, DOWN, buff=0.5).shift(LEFT * 1.6)

        self.play(Create(check), Write(check[1]), FadeIn(check[2]))
        self.play(Create(interact), Write(interact[1]), FadeIn(interact[2]))
        self.play(Create(effect), Write(effect[1]), FadeIn(effect[2]))
        self.wait(0.5)

        # The re-entrant loop
        attacker = RoundedRectangle(
            width=2.4, height=1.0, corner_radius=0.15, color=RED
        )
        attacker_label = Text("Attacker\nfallback()", color=RED).scale(0.35)
        attacker_label.move_to(attacker.get_center())
        attacker_group = VGroup(attacker, attacker_label)
        attacker_group.next_to(steps, RIGHT, buff=1.0).shift(UP * 0.3)

        self.play(FadeIn(attacker_group))

        reenter = Arrow(
            attacker.get_bottom(),
            check.get_right(),
            color=RED,
            buff=0.15,
        )
        reenter_label = Text("re-enters!", color=RED).scale(0.35)
        reenter_label.next_to(reenter, DOWN, buff=0.1)

        self.play(Indicate(interact[1], color=RED))
        self.play(Create(reenter), FadeIn(reenter_label))
        self.play(Indicate(check, color=RED))
        self.wait(0.4)

        drain = Text("Balance still > 0 -> drained in a loop", color=RED)
        drain.scale(0.42).next_to(steps, DOWN, buff=0.5)
        self.play(Write(drain))
        self.play(Indicate(reenter, color=RED), Indicate(interact, color=RED))
        self.wait(2)

        self.attack_group = VGroup(
            heading, steps, attacker_group, reenter, reenter_label, drain
        )
        self.play(FadeOut(self.attack_group))

    # ------------------------------------------------------------------
    # 4. DEFENSE — CORRECT CEI ORDERING
    # ------------------------------------------------------------------
    def show_defense(self):
        heading = Text("Defense: update state BEFORE the external call", color=GREEN)
        heading.scale(0.5).to_edge(UP)
        self.play(Write(heading))

        check = self.make_step(
            "1. CHECK", "require(balance[attacker] > 0)", YELLOW
        )
        effect = self.make_step(
            "2. EFFECT", "balance[attacker] = 0   <-- state cleared", GREEN
        )
        interact = self.make_step(
            "3. INTERACT", "attacker.call{value: bal}('')", GREEN
        )

        steps = VGroup(check, effect, interact).arrange(DOWN, buff=0.5)
        steps.next_to(heading, DOWN, buff=0.6).shift(LEFT * 1.4)

        self.play(Create(check), Write(check[1]), FadeIn(check[2]))
        self.play(Create(effect), Write(effect[1]), FadeIn(effect[2]))
        self.play(Create(interact), Write(interact[1]), FadeIn(interact[2]))

        a1 = Arrow(check.get_bottom(), effect.get_top(), color=GREEN, buff=0.1)
        a2 = Arrow(effect.get_bottom(), interact.get_top(), color=GREEN, buff=0.1)
        self.play(Create(a1), Create(a2))

        # Re-entry now fails the check
        attacker = RoundedRectangle(
            width=2.4, height=1.0, corner_radius=0.15, color=GREY
        )
        attacker_label = Text("Attacker\nfallback()", color=GREY).scale(0.35)
        attacker_label.move_to(attacker.get_center())
        attacker_group = VGroup(attacker, attacker_label)
        attacker_group.next_to(steps, RIGHT, buff=1.0)

        reenter = Arrow(attacker.get_left(), check.get_right(), color=GREEN, buff=0.15)
        blocked = Text("balance == 0 -> require() reverts", color=GREEN).scale(0.35)
        blocked.next_to(reenter, UP, buff=0.15)

        self.play(FadeIn(attacker_group), Create(reenter))
        self.play(Write(blocked))
        self.play(Indicate(check, color=GREEN), Indicate(effect, color=GREEN))
        self.wait(0.5)

        guard = Text(
            "Belt & suspenders: add a nonReentrant lock too",
            color=GREEN,
        ).scale(0.4)
        guard.next_to(steps, DOWN, buff=0.5)
        self.play(FadeIn(guard))
        self.wait(2)

        self.defense_group = VGroup(
            heading, steps, a1, a2, attacker_group, reenter, blocked, guard
        )
        self.play(FadeOut(self.defense_group))

    # ------------------------------------------------------------------
    # 5. SUMMARY / KEY TAKEAWAYS
    # ------------------------------------------------------------------
    def show_summary(self):
        title = Text("Key takeaways", color=BLUE).scale(0.7).to_edge(UP)
        self.play(Write(title))

        points = [
            "Order matters: Checks -> Effects -> Interactions",
            "Never make an external call before updating state",
            "CEI alone does not stop every variant:",
            "   read-only, cross-function, cross-contract, callback-hook",
            "Add nonReentrant guards on ALL shared-state entrypoints",
            "Guard views too -- read-only reentrancy reads stale state",
        ]

        colors = [GREEN, GREEN, YELLOW, YELLOW, GREEN, RED]
        items = VGroup()
        for text, color in zip(points, colors):
            line = Text(text, color=color).scale(0.42)
            items.add(line)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        items.next_to(title, DOWN, buff=0.6)

        for line in items:
            self.play(FadeIn(line), run_time=0.5)
        self.wait(1)

        box = RoundedRectangle(
            width=items.width + 0.8,
            height=items.height + 0.6,
            corner_radius=0.2,
            color=BLUE,
        )
        box.move_to(items.get_center())
        self.play(Create(box))

        footer = Text("$80M+ lost to reentrancy variants, 2022-2024", color=RED)
        footer.scale(0.4).next_to(box, DOWN, buff=0.4)
        self.play(Write(footer))
        self.wait(3)

        self.play(
            FadeOut(title), FadeOut(items), FadeOut(box), FadeOut(footer)
        )
        self.wait(0.5)