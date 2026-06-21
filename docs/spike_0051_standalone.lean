/-
STANDALONE test of hard2_0051 (Eq2531 ⊬ Eq4307) — INFINITE algebraic model.
v2: carrier is ℝ (a field) instead of AdjoinRoot, so division and `1 ≠ 0`
are free (v1 hit `HDiv F F` and `NeZero 1` because AdjoinRoot is only a CommRing).
We get a real root α of p = X⁴−X³−X²+X−1 via the intermediate value theorem
(p 1 = −1 < 0 < 5 = p 2), then op x y = α·x + (1−α)·y.

The eq1 / eq2 proofs are unchanged in spirit (each is one `linear_combination`);
v1 already showed `hp`-style derivation and the eq1 half compile.  Report any
error and I'll patch the IVT plumbing — the algebra is verified.
-/
import Mathlib

open Polynomial Set

class Magma (α : Type _) where
  op : α → α → α
@[inherit_doc] infix:65 " ◇ " => Magma.op

theorem spike_0051 :
    ∃ (G : Type) (_ : Magma G),
      (∀ x y : G, x = (y ◇ ((y ◇ x) ◇ x)) ◇ y) ∧
      ¬ (∀ x y z : G, x ◇ (x ◇ y) = z ◇ (z ◇ y)) := by
  -- a real root α of p = X⁴ − X³ − X² + X − 1, via IVT on [1,2]
  obtain ⟨α, -, hp⟩ :
      ∃ α ∈ Icc (1 : ℝ) 2, α ^ 4 - α ^ 3 - α ^ 2 + α - 1 = 0 := by
    have hc : ContinuousOn (fun t : ℝ => t ^ 4 - t ^ 3 - t ^ 2 + t - 1) (Icc 1 2) := by
      fun_prop
    have hsub := intermediate_value_Icc (by norm_num : (1 : ℝ) ≤ 2) hc
    have hmem : (0 : ℝ) ∈
        Icc ((fun t : ℝ => t ^ 4 - t ^ 3 - t ^ 2 + t - 1) 1)
            ((fun t : ℝ => t ^ 4 - t ^ 3 - t ^ 2 + t - 1) 2) := by
      norm_num
    simpa using hsub hmem
  refine ⟨ℝ, ⟨fun x y => α * x + (1 - α) * y⟩, ?_, ?_⟩
  · -- eq1:  x = (y ◇ ((y ◇ x) ◇ x)) ◇ y     (RHS − x = p(α)·(x − y) = 0)
    intro x y
    show x = α * (α * y + (1 - α) * (α * (α * y + (1 - α) * x) + (1 - α) * x))
              + (1 - α) * y
    linear_combination (y - x) * hp
  · -- ¬ eq2:  witness (x,y,z) = (1,0,0) would force 2α − α² = 0, impossible
    intro h
    have h2 : α * 1 + (1 - α) * (α * 1 + (1 - α) * 0)
            = α * 0 + (1 - α) * (α * 0 + (1 - α) * 0) := h 1 0 0
    have hcontra : (1 : ℝ) = 0 := by
      linear_combination (3 * α / 5 - 1) * hp
        + (3 * α ^ 3 / 5 - 2 * α ^ 2 / 5 - 2 * α / 5 + 4 / 5) * h2
    exact one_ne_zero hcontra
