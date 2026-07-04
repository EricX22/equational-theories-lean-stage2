% order5v2_1029  eq1=34503 eq2=56058  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,f(U,U))),W) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,Y)) != f(f(Z,W),f(W,W)) )).
