import JudgeMagma.Magma
import JudgeDecide.DecideBang
import JudgeFinOp.MemoFinOp

open MemoFinOp

-- Example local false-style finite magma check.
example : True := by
  let m : Magma (Fin 2) := {
    op := finOpTable "[[0,0],[1,1]]"
  }
  trivial

-- Example local true-style proof shape.
example
    (G : Type) [Magma G]
    (h : ∀ x y : G, x = x ◇ y)
    : ∀ x y : G, x = x ◇ y := by
  intro x y
  exact h x y

-- Reverse direction using .symm
example
    (G : Type) [Magma G]
    (h : ∀ x y : G, x = x ◇ y)
    : ∀ x y : G, x ◇ y = x := by
  intro x y
  exact (h x y).symm
