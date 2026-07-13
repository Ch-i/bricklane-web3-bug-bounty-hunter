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
        title = Text("Signature Replay", color=WHITE, weight=BOLD).scale(1.2)
        subtitle = Text("& EIP-712 Typed Data", color=BLUE).scale(0.8)
        tag = Text("web3 security pattern", color=GREY).scale(0.45)

        title.move_to(UP * 0.8)
        subtitle.next_to(title, DOWN, buff=0.4)
        tag.next_to(subtitle, DOWN, buff=0.6)

        box = RoundedRectangle(
            width=10, height=4.5, corner_radius=0.3, color=BLUE
        )

        self.play(Create(box))
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP * 0.3))
        self.play(FadeIn(tag))
        self.wait(1.5)
        self.play(FadeOut(VGroup(box, title, subtitle, tag)))

    # ------------------------------------------------------------------
    # 2. Core logic step-by-step
    # ------------------------------------------------------------------
    def core_logic(self):
        header = Text("Core Logic: Off-chain sign, on-chain act", color=WHITE).scale(0.6)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header))

        digest = MathTex(
            r"\text{digest} = \text{keccak256}(\texttt{0x1901} \,\|\, "
            r"\text{domainSep} \,\|\, \text{hashStruct}(m))",
            color=YELLOW,
        ).scale(0.7)
        digest.next_to(header, DOWN, buff=0.6)
        self.play(Write(digest))
        self.wait(0.5)

        # The four binding dimensions
        dims = [
            ("uniqueness", "nonce -> one-time use", BLUE),
            ("chain", "chainId -> one chain", BLUE),
            ("domain", "verifyingContract -> one deployment", BLUE),
            ("content", "struct hash -> every field", BLUE),
        ]
        rows = VGroup()
        for name, desc, col in dims:
            label = Text(name, color=col).scale(0.5)
            arrow = Text(":", color=GREY).scale(0.5)
            body = Text(desc, color=WHITE).scale(0.45)
            row = VGroup(label, arrow, body).arrange(RIGHT, buff=0.25)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        rows.next_to(digest, DOWN, buff=0.7)

        bind_box = RoundedRectangle(
            width=rows.width + 1.0,
            height=rows.height + 0.8,
            corner_radius=0.2,
            color=GREEN,
        ).move_to(rows)

        self.play(Create(bind_box))
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(1.0)

        recover = MathTex(
            r"\text{signer} = \text{ecrecover}(\text{digest},\, v, r, s)",
            color=WHITE,
        ).scale(0.6)
        recover.next_to(bind_box, DOWN, buff=0.5)
        self.play(Write(recover))
        self.wait(1.0)

        self.play(
            FadeOut(VGroup(header, digest, rows, bind_box, recover))
        )

    # ------------------------------------------------------------------
    # 3. Attack / vulnerability flow
    # ------------------------------------------------------------------
    def attack_flow(self):
        header = Text("Vulnerability: Replay", color=RED).scale(0.7)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header))

        note = Text(
            "Nonce in message, but never enforced",
            color=RED,
        ).scale(0.45)
        note.next_to(header, DOWN, buff=0.3)
        self.play(FadeIn(note))

        sig = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.15, color=YELLOW)
        sig_label = Text("valid sig", color=YELLOW).scale(0.45).move_to(sig)
        sig_group = VGroup(sig, sig_label).to_edge(LEFT, buff=1.0).shift(DOWN * 0.5)

        contract = Rectangle(width=3.0, height=1.4, color=WHITE)
        c_label = Text("contract", color=WHITE).scale(0.45).move_to(contract)
        contract_group = VGroup(contract, c_label).move_to(RIGHT * 3.0 + DOWN * 0.5)

        self.play(Create(sig_group), Create(contract_group))

        # Replay it three times
        prev = None
        for i in range(3):
            a = Arrow(
                start=sig.get_right(),
                end=contract.get_left(),
                color=RED,
                buff=0.2,
            ).shift(UP * (0.5 - i * 0.5))
            tag = Text(f"replay #{i + 1}", color=RED).scale(0.35)
            tag.next_to(a, UP, buff=0.05)
            self.play(Create(a), FadeIn(tag), run_time=0.6)
            self.play(Indicate(contract_group, color=RED), run_time=0.5)
            prev = VGroup(a, tag) if prev is None else VGroup(prev, a, tag)

        result = Text("same sig executes again and again", color=RED).scale(0.5)
        result.to_edge(DOWN, buff=0.8)
        self.play(Write(result))
        self.play(Indicate(result, color=RED, scale_factor=1.15))
        self.wait(1.2)

        self.play(
            FadeOut(VGroup(header, note, sig_group, contract_group, prev, result))
        )

    # ------------------------------------------------------------------
    # 4. Defense pattern
    # ------------------------------------------------------------------
    def defense_pattern(self):
        header = Text("Defense: Enforce the nonce", color=GREEN).scale(0.7)
        header.to_edge(UP, buff=0.5)
        self.play(Write(header))

        steps = [
            "1.  recover signer from EIP-712 digest",
            "2.  require(nonce == expected[signer])",
            "3.  expected[signer] += 1   (consume it)",
            "4.  bind chainId + verifyingContract",
        ]
        lines = VGroup()
        for s in steps:
            lines.add(Text(s, color=WHITE).scale(0.5))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        lines.next_to(header, DOWN, buff=0.7)

        guard_box = RoundedRectangle(
            width=lines.width + 1.0,
            height=lines.height + 0.8,
            corner_radius=0.2,
            color=GREEN,
        ).move_to(lines)

        self.play(Create(guard_box))
        for line in lines:
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=0.5)

        # Highlight the critical check
        self.play(Indicate(lines[1], color=GREEN, scale_factor=1.1))
        self.wait(0.5)

        # Second replay attempt now reverts
        revert = Text("second use -> revert: stale nonce", color=GREEN).scale(0.5)
        revert.next_to(guard_box, DOWN, buff=0.6)
        self.play(Write(revert))
        self.play(Indicate(revert, color=GREEN, scale_factor=1.15))
        self.wait(1.2)

        self.play(FadeOut(VGroup(header, lines, guard_box, revert)))

    # ------------------------------------------------------------------
    # 5. Summary
    # ------------------------------------------------------------------
    def summary(self):
        header = Text("Key Takeaways", color=YELLOW, weight=BOLD).scale(0.8)
        header.to_edge(UP, buff=0.6)
        self.play(Write(header))

        takeaways = [
            ("Bind 4 dimensions", "uniqueness, chain, domain, content", GREEN),
            ("Partial nonce = bug", "increment without require(==) still replays", RED),
            ("Don't freeze domainSep", "re-check chainId after a hard fork", RED),
            ("ecrecover hygiene", "no abi.encodePacked collisions, no reused k", BLUE),
        ]
        cards = VGroup()
        for title, desc, col in takeaways:
            t = Text(title, color=col, weight=BOLD).scale(0.5)
            d = Text(desc, color=WHITE).scale(0.4)
            grp = VGroup(t, d).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            box = RoundedRectangle(
                width=11.0,
                height=grp.height + 0.5,
                corner_radius=0.15,
                color=col,
            )
            grp.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.4)
            cards.add(VGroup(box, grp))
        cards.arrange(DOWN, buff=0.35)
        cards.next_to(header, DOWN, buff=0.6)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.2), run_time=0.6)
        self.wait(2.0)

        self.play(FadeOut(VGroup(header, cards)))
        self.wait(0.5)