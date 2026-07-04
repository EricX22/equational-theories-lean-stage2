% order5v2_1441  eq1=36063 eq2=5168  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,Z)),f(X,W)),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Y,f(Z,f(Z,f(Z,W))))) )).
