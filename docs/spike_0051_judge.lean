/-
JUDGE-format false certificate for hard2_0051 (Equation2531 ⊬ Equation4307).
Submit this whole file as the `code` of a `verdict:"false"` judge call.

Same proof that compiled standalone, ported to the judge contract:
  - `import JudgeProblem` provides `Goal`, `Magma`, and `◇` (so we DON'T redefine them),
  - `import Mathlib` provides IVT + `linear_combination` (the one thing left to confirm
    is that the judge env allows importing Mathlib in a submission).

Model: G = ℝ, x ◇ y = α·x + (1−α)·y, α a real root of X⁴−X³−X²+X−1 (via IVT).
eq1 holds (RHS−x = p(α)(x−y) = 0); eq2 fails (witness (1,0,0) ⇒ 2α−α² = 0, impossible).
-/
import JudgeProblem
import Mathlib

open Polynomial Set

def submission : Goal := by
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
  refine ⟨ℝ, { op := fun x y => α * x + (1 - α) * y }, ?_, ?_⟩
  · intro x y
    show x = α * (α * y + (1 - α) * (α * (α * y + (1 - α) * x) + (1 - α) * x))
              + (1 - α) * y
    linear_combination (y - x) * hp
  · intro h
    have h2 : α * 1 + (1 - α) * (α * 1 + (1 - α) * 0)
            = α * 0 + (1 - α) * (α * 0 + (1 - α) * 0) := h 1 0 0
    have hcontra : (1 : ℝ) = 0 := by
      linear_combination (3 * α / 5 - 1) * hp
        + (3 * α ^ 3 / 5 - 2 * α ^ 2 / 5 - 2 * α / 5 + 4 / 5) * h2
    exact one_ne_zero hcontra
