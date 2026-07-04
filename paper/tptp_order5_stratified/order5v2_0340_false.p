% order5v2_0340  eq1=22105 eq2=60116  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,W)),f(X,f(Z,Y))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(f(X,X),Y) != f(f(Z,Z),f(Z,Z)) )).
