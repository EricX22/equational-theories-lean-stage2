% order5v2_0634  eq1=37127 eq2=20357  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),f(U,W)),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,Z),f(f(W,f(X,W)),Z)) )).
