/-
SPIKE: false certificate for hard2_0051  (Equation2531 ⊬ Equation4307)
via an INFINITE algebraic model — the capability finite search can't reach.

Model (found deterministically; verified numerically + symbolically):
  carrier  G = ℚ(α),  α a root of  p = X⁴ − X³ − X² + X − 1   (α ≈ −1.1787)
  operation  x ◇ y = α·x + (1−α)·y         (a weighted average; α irrational)

Why it works (both verified in Python, exact):
  • eq1  `x = (y ◇ ((y ◇ x) ◇ x)) ◇ y`  holds because RHS − x = p(α)·(x − y),
    and p(α) = 0.   ⇒  proof is  `linear_combination (y - x) * hp`.
  • eq2  `x ◇ (x ◇ y) = z ◇ (z ◇ y)`  FAILS: at (x,y,z)=(1,0,0) it would force
    2α − α² = 0, but p and (2X − X²) are coprime, with Bézout identity
       (3α/5 − 1)·p(α) + (3α³/5 − 2α²/5 − 2α/5 + 4/5)·(2α − α²) = 1.
    Assuming eq2 then gives 1 = 0.   ⇒ `linear_combination` with those coeffs.

This is a SPIKE to answer one binary question: can the judge verify an
infinite/algebraic model at all?  The mathematics above is solid; the THREE
Lean-side risk points (in order of importance) are:
  (1) Does the judge env allow `import Mathlib...` / `AdjoinRoot`?  ← make-or-break
  (2) The `hp` derivation lemma name (AdjoinRoot API drift).
  (3) Unfolding `◇` (the `show`/`rfl` steps) so `linear_combination`/`ring` see
      the polynomial form.
If (1) fails, the whole algebraic-model avenue is dead for the competition and
we stop; if it passes, this pipeline can be automated to crack a class of hard
non-implications no finite searcher can touch.
-/
import JudgeProblem
import Mathlib.RingTheory.AdjoinRoot   -- (1) the make-or-break import

open Polynomial

noncomputable def pf : ℚ[X] := X ^ 4 - X ^ 3 - X ^ 2 + X - 1
noncomputable abbrev F : Type := AdjoinRoot pf
noncomputable def α : F := AdjoinRoot.root pf

noncomputable instance : Magma F := ⟨fun x y => α * x + (1 - α) * y⟩

def submission : Goal := by
  -- (2) the defining relation p(α) = 0
  have hp : α ^ 4 - α ^ 3 - α ^ 2 + α - 1 = 0 := by
    have h0 : (AdjoinRoot.mk pf) pf = 0 := AdjoinRoot.mk_self
    simpa [pf, α, AdjoinRoot.root, map_sub, map_add, map_one, map_pow]
      using h0
  refine ⟨F, inferInstance, ?_, ?_⟩
  · -- eq1 holds:  x = (y ◇ ((y ◇ x) ◇ x)) ◇ y
    intro x y
    -- (3) unfold ◇ to the polynomial form (definitional for our op)
    show x = α * (α * y + (1 - α) * (α * (α * y + (1 - α) * x) + (1 - α) * x))
              + (1 - α) * y
    linear_combination (y - x) * hp
  · -- ¬ eq2:  ¬ ∀ x y z, x ◇ (x ◇ y) = z ◇ (z ◇ y)
    intro h
    have h2 : α * 1 + (1 - α) * (α * 1 + (1 - α) * 0)
            = α * 0 + (1 - α) * (α * 0 + (1 - α) * 0) := h 1 0 0   -- ◇ unfolds by rfl
    have hcontra : (1 : F) = 0 := by
      linear_combination (3 * α / 5 - 1) * hp
        + (3 * α ^ 3 / 5 - 2 * α ^ 2 / 5 - 2 * α / 5 + 4 / 5) * h2
    exact one_ne_zero hcontra
