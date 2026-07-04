% order5v2_0500  eq1=10407 eq2=36142  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Y,Z),f(f(Y,Y),Y))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,f(Z,W)),f(X,W)),Y) )).
