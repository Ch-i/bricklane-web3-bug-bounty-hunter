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
        title = Text("Access Control Hierarchies", color=BLUE).scale(0.9)
        subtitle = Text("& Role Systems", color=WHITE).scale(0.7)
        domain = Text("web3 security pattern", color=GREY).scale(0.4)

        subtitle.next_to(title, DOWN, buff=0.3)
        domain.next_to(subtitle, DOWN, buff=0.4)

        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.play(FadeIn(domain))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(domain))

    # ------------------------------------------------------------------
    # 2. Core logic, step by step
    # ------------------------------------------------------------------
    def show_core_logic(self):
        heading = Text("The Authorization Gate", color=BLUE).scale(0.6)
        heading.to_edge(UP)
        self.play(Write(heading))

        caller = Rectangle(width=2.6, height=1.0, color=WHITE)
        caller_label = Text("caller (EOA)", color=WHITE).scale(0.4).move_to(caller)
        caller_grp = VGroup(caller, caller_label).to_edge(LEFT, buff=1.0)

        gate = RoundedRectangle(width=3.0, height=1.4, color=YELLOW, corner_radius=0.2)
        gate_label = Text("onlyOwner\ncheck", color=YELLOW).scale(0.4).move_to(gate)
        gate_grp = VGroup(gate, gate_label)

        state = Rectangle(width=2.8, height=1.0, color=GREEN)
        state_label = Text("privileged\nstate", color=GREEN).scale(0.4).move_to(state)
        state_grp = VGroup(state, state_label).to_edge(RIGHT, buff=1.0)

        a1 = Arrow(caller_grp.get_right(), gate_grp.get_left(), color=WHITE, buff=0.2)
        a2 = Arrow(gate_grp.get_right(), state_grp.get_left(), color=WHITE, buff=0.2)

        self.play(Create(caller_grp))
        self.play(Create(gate_grp))
        self.play(Create(state_grp))
        self.play(Create(a1), Create(a2))

        note = Text(
            "require(msg.sender == owner)",
            color=WHITE,
        ).scale(0.45)
        note.next_to(gate_grp, DOWN, buff=1.0)
        self.play(Write(note))
        self.play(Indicate(gate_grp, color=YELLOW))
        self.wait(1.5)

        self.core_group = VGroup(
            heading, caller_grp, gate_grp, state_grp, a1, a2, note
        )
        self.play(FadeOut(self.core_group))

    # ------------------------------------------------------------------
    # 3. Attack / vulnerability flow (red)
    # ------------------------------------------------------------------
    def show_attack_flow(self):
        heading = Text("Vulnerability: Missing / Wrong Gate", color=RED).scale(0.55)
        heading.to_edge(UP)
        self.play(Write(heading))

        attacker = Rectangle(width=2.6, height=1.0, color=RED)
        attacker_label = Text("attacker EOA", color=RED).scale(0.4).move_to(attacker)
        attacker_grp = VGroup(attacker, attacker_label).to_edge(LEFT, buff=1.0)

        gate = RoundedRectangle(width=3.0, height=1.4, color=RED, corner_radius=0.2)
        gate_label = Text("no modifier\n(refactored out)", color=RED).scale(0.38).move_to(gate)
        gate_grp = VGroup(gate, gate_label)

        state = Rectangle(width=2.8, height=1.0, color=RED)
        state_label = Text("fees / owner\nseized", color=RED).scale(0.4).move_to(state)
        state_grp = VGroup(state, state_label).to_edge(RIGHT, buff=1.0)

        a1 = Arrow(attacker_grp.get_right(), gate_grp.get_left(), color=RED, buff=0.2)
        a2 = Arrow(gate_grp.get_right(), state_grp.get_left(), color=RED, buff=0.2)

        self.play(Create(attacker_grp))
        self.play(Create(gate_grp), Create(a1))
        self.play(Indicate(gate_grp, color=RED))
        self.play(Create(a2), Create(state_grp))

        failures = VGroup(
            Text("• setter with no onlyOwner / onlyRole", color=RED).scale(0.4),
            Text("• tx.origin instead of msg.sender", color=RED).scale(0.4),
            Text("• unprotected initialize() / _authorizeUpgrade", color=RED).scale(0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        failures.next_to(gate_grp, DOWN, buff=1.0)
        self.play(Write(failures))
        self.play(Indicate(state_grp, color=RED))
        self.wait(1.5)

        self.attack_group = VGroup(
            heading, attacker_grp, gate_grp, state_grp, a1, a2, failures
        )
        self.play(FadeOut(self.attack_group))

    # ------------------------------------------------------------------
    # 4. Defense pattern (green)
    # ------------------------------------------------------------------
    def show_defense(self):
        heading = Text("Defense: Consistent Role Enforcement", color=GREEN).scale(0.55)
        heading.to_edge(UP)
        self.play(Write(heading))

        checks = VGroup(
            Text("✓ Gate every privileged setter with onlyRole / onlyOwner", color=GREEN).scale(0.42),
            Text("✓ Always check msg.sender, never tx.origin", color=GREEN).scale(0.42),
            Text("✓ Protect initialize() with initializer modifier", color=GREEN).scale(0.42),
            Text("✓ Override inherited grantRole / revokeRole wrappers", color=GREEN).scale(0.42),
            Text("✓ Use a timelock + multisig, not a single key", color=GREEN).scale(0.42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        checks.next_to(heading, DOWN, buff=0.6)

        box = RoundedRectangle(
            width=checks.width + 0.8,
            height=checks.height + 0.6,
            color=GREEN,
            corner_radius=0.2,
        ).move_to(checks)

        self.play(Create(box))
        for line in checks:
            self.play(FadeIn(line), run_time=0.5)
        self.play(Indicate(box, color=GREEN))
        self.wait(1.5)

        self.defense_group = VGroup(heading, box, checks)
        self.play(FadeOut(self.defense_group))

    # ------------------------------------------------------------------
    # 5. Summary / takeaways
    # ------------------------------------------------------------------
    def show_summary(self):
        title = Text("Key Takeaways", color=YELLOW).scale(0.7).to_edge(UP)
        self.play(Write(title))

        points = VGroup(
            Text("1. Access control bugs are the #1 high/critical finding.", color=WHITE).scale(0.45),
            Text("2. Check three modes: missing, wrong principal, structural bypass.", color=WHITE).scale(0.45),
            Text("3. Unprotected initializers hand ownership to the first caller.", color=WHITE).scale(0.45),
            Text("4. The owner key itself is a single point of failure.", color=WHITE).scale(0.45),
            Text("5. Enforce roles consistently across base + derived contracts.", color=WHITE).scale(0.45),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        points.next_to(title, DOWN, buff=0.7)

        for p in points:
            self.play(FadeIn(p), run_time=0.5)

        self.wait(1.0)
        closing = Text("Authorize every state change. Verify the principal.", color=GREEN).scale(0.5)
        closing.next_to(points, DOWN, buff=0.7)
        self.play(Write(closing))
        self.play(Indicate(closing, color=GREEN))
        self.wait(2.0)
        self.play(FadeOut(title), FadeOut(points), FadeOut(closing))