% order5v2_1063  eq1=8513 eq2=55064  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(Y,f(X,f(f(f(Z,Y),W),U))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Y)) != f(X,f(f(Z,Y),Z)) )).
