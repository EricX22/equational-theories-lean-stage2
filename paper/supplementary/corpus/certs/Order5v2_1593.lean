/-
Counter-model certificate for the open order-5 pair `order5v2_1593`.

  EQ1 (must HOLD):   x = ((y ◇ z) ◇ (z ◇ x)) ◇ (z ◇ y)
  EQ2 (must FAIL):   x = y ◇ (x ◇ ((z ◇ x) ◇ (w ◇ u)))

Witness magma:  G = ZMod 17,  a ◇ b = 8*a + 7*b  (mod 17).

This is a fully *symbolic* certificate: it is verified by Lean's kernel with no
enumeration at all. EQ1 is proved as a universal integer-polynomial identity
plus one modulus fact via `linear_combination` (cost independent of the modulus
AND of the number of variables). EQ2 is refuted by a single explicit witness
(x=1, y=z=w=u=0 gives 1 = 12 in ZMod 17). So we never touch the 17^3 ground
cases `decide` would check for EQ1, nor the 17^5 space that makes an explicit-
table `decideFin` time out for EQ2.

(An earlier version of this cert proved EQ1 with `decide`; it PASSED but took
161s in the kernel -- above the competition judge's 120s cap, which is exactly
why the judge rejected this correct model. The symbolic proof below is ~instant
and, unlike `decide`, scales to EQ1s with 4-5 variables.)

Proposed by openai/o3 (family "mod17-affine"); it lives outside the solver's
own affine search, which caps n so that n^(#vars) <= 400000 (=> n <= 13 for a
5-variable equation), hence n=17 is structurally unreachable to the solver.

Soundness: proofs use only `decide` (kernel-checked); NOT `native_decide`.
Verify axiom footprint with `#print axioms` (appended at the bottom).
-/
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.LinearCombination

set_option maxRecDepth 100000

namespace Order5v2_1593

abbrev G : Type := ZMod 17

/-- The witness operation: `a ◇ b = 8·a + 7·b` over `ZMod 17`. -/
def op (a b : G) : G := 8 * a + 7 * b

/-- EQ1 holds in `(G, op)` for every `x y z`.

    Symbolic proof: `RHS - x` expands to `391·x + 561·y + 952·z`, and every
    coefficient is a multiple of 17, so `RHS - x = 17·(23·x + 33·y + 56·z)`,
    which is `0` in `ZMod 17`. The correction coefficients
    `(23, 33, 56) = (391, 561, 952) / 17` are exactly
    `(RHS_coeff_v - LHS_coeff_v) / n` per variable `v` -- the same data the
    solver's `af_eval` already computes -- so this construction is mechanical
    for any affine model over any modulus and any number of variables. -/
theorem eq1_holds : ∀ x y z : G, x = op (op (op y z) (op z x)) (op z y) := by
  intro x y z
  have h17 : (17 : G) = 0 := by decide
  simp only [op]
  linear_combination (-(23 * x + 33 * y + 56 * z)) * h17

/-- EQ2 fails in `(G, op)`: the assignment `x=1, y=z=w=u=0` gives `1 = 12`. -/
theorem eq2_fails :
    ¬ ∀ x y z w u : G, x = op y (op x (op (op z x) (op w u))) := by
  intro h
  exact absurd (h 1 0 0 0 0) (by decide)

/-- The pair is separated by this magma: EQ1 holds and EQ2 does not. -/
theorem separates :
    (∀ x y z : G, x = op (op (op y z) (op z x)) (op z y)) ∧
    ¬ (∀ x y z w u : G, x = op y (op x (op (op z x) (op w u)))) :=
  ⟨eq1_holds, eq2_fails⟩

end Order5v2_1593

#print axioms Order5v2_1593.eq1_holds
#print axioms Order5v2_1593.eq2_fails
#print axioms Order5v2_1593.separates
