% order5v2_0736  eq1=279 eq2=7559  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,X),Z),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(X,f(f(X,f(Z,Z)),Z))) )).
