/-
  POSITIVE CONTROL 2 — the congrArg shape the autoformalizer emits.

  `trivial_autoform.justify_step` emits congruence steps as
      congrArg (fun z => op z R) (<sub-proof>)      -- rewrite inside the LEFT child
      congrArg (fun z => op L z) (<sub-proof>)      -- rewrite inside the RIGHT child
  The toy law used in positive_control.lean CANNOT exercise this (its RHS has no `x`, so every
  step justifies as a whole-term application instead). These standalone examples check that the
  emitted shape type-checks. Plain Lean, no Mathlib, no Problem header needed.

  If these AND positive_control.lean are accepted, the assembler's full output vocabulary is
  validated, and any model scoring 0 is a genuine model failure rather than a harness artifact.
-/

-- left-child congruence:  from  a = op a a  conclude  op a c = op (op a a) c
example (M : Type) (op : M → M → M) (h : ∀ x y : M, x = op y y) (a c : M) :
    op a c = op (op a a) c :=
  congrArg (fun z => op z c) (h a a)

-- right-child congruence: from  a = op a a  conclude  op c a = op c (op a a)
example (M : Type) (op : M → M → M) (h : ∀ x y : M, x = op y y) (a c : M) :
    op c a = op c (op a a) :=
  congrArg (fun z => op c z) (h a a)

-- nested (depth-2) congruence, as produced for a rewrite two levels down
example (M : Type) (op : M → M → M) (h : ∀ x y : M, x = op y y) (a c d : M) :
    op (op a c) d = op (op (op a a) c) d :=
  congrArg (fun z => op z d) (congrArg (fun z => op z c) (h a a))
