/-
Counter-model certificate for the open order-5 pair `order5v2_1593`.

  EQ1 (must HOLD):   x = ((y ◇ z) ◇ (z ◇ x)) ◇ (z ◇ y)
  EQ2 (must FAIL):   x = y ◇ (x ◇ ((z ◇ x) ◇ (w ◇ u)))

Witness magma:  G = ZMod 17,  a ◇ b = 8*a + 7*b  (mod 17).

This is a *symbolic* certificate: it is verified by Lean's kernel directly.
EQ1 is a universally-quantified statement in 3 variables (17^3 = 4913 ground
cases, well within `decide`). EQ2 is refuted by a single explicit witness
(x=1, y=z=w=u=0 gives 1 = 12 in ZMod 17), so we never enumerate the 17^5
assignment space that makes an explicit-table `decideFin` time out.

Proposed by openai/o3 (family "mod17-affine"); it lives outside the solver's
own affine search, which caps n so that n^(#vars) <= 400000 (=> n <= 13 for a
5-variable equation), hence n=17 is structurally unreachable to the solver.

Soundness: proofs use only `decide` (kernel-checked); NOT `native_decide`.
Verify axiom footprint with `#print axioms` (appended at the bottom).
-/
import Mathlib.Data.ZMod.Basic

set_option maxRecDepth 100000

namespace Order5v2_1593

abbrev G : Type := ZMod 17

/-- The witness operation: `a ◇ b = 8·a + 7·b` over `ZMod 17`. -/
def op (a b : G) : G := 8 * a + 7 * b

/-- EQ1 holds in `(G, op)` for every `x y z`. -/
theorem eq1_holds : ∀ x y z : G, x = op (op (op y z) (op z x)) (op z y) := by
  decide

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
