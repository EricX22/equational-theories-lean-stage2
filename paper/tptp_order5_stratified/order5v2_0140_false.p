% order5v2_0140  eq1=24263 eq2=54902  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,X),Y),f(f(Z,W),Z)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,X)) != f(X,f(f(Y,Y),Z)) )).
