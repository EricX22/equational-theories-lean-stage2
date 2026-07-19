set_option maxRecDepth 8000 in
theorem solution : Problem.TrivialGoal := by
  intro M op h a b
  calc a = (op a a) := h a a
    _ = b := (h b a).symm
