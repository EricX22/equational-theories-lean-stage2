/-
  Problem statement. GENERATED — do not edit, do not redefine in a submission.

    law:  x = (((w ◇ y) ◇ (((x ◇ y) ◇ z) ◇ x)) ◇ y)

  Exactly one of `AustinGoal` and `TrivialGoal` is true, given the separately
  machine-checked fact that this law admits no nontrivial FINITE model.
-/
namespace Problem

/-- A magma satisfying the law. -/
def Law {M : Type} (op : M → M → M) : Prop :=
  ∀ x w y z : M, x = (op (op (op w y) (op (op (op x y) z) x)) y)

/-- There is a nontrivial model. (It is then necessarily infinite.) -/
def AustinGoal : Prop :=
  ∃ (M : Type) (op : M → M → M), (∃ a b : M, a ≠ b) ∧ Law op

/-- Every model collapses. Equivalently `law ⊨ x = y`. -/
def TrivialGoal : Prop :=
  ∀ (M : Type) (op : M → M → M), Law op → ∀ a b : M, a = b

end Problem

set_option maxRecDepth 8000 in
theorem solution : Problem.TrivialGoal := by
  intro M op h a b
  calc a = (op (op (op b b) (op (op (op a b) a) a)) b) := h a b b a
    _ = (op (op (op b b) (op (op (op b b) (op (op (op (op (op (op a b) a) a) b) a) (op (op (op a b) a) a))) b)) b) := congrArg (fun z => op z b) (congrArg (fun z => op (op b b) z) (h (op (op (op a b) a) a) b b a))
    _ = b := (h b b b (op (op (op (op (op (op a b) a) a) b) a) (op (op (op a b) a) a))).symm


-- GENERATED. Forces `solution` to have exactly the type we asked for.
example : Problem.TrivialGoal := solution

#print axioms solution
