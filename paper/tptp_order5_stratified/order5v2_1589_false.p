% order5v2_1589  eq1=29754 eq2=46986  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(Y,f(Y,f(Z,f(W,U)))),U) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,X) != f(f(Y,Z),f(f(W,W),W)) )).
