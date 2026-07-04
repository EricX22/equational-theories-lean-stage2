% order5v2_0119  eq1=38790 eq2=42653  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(f(Z,W),Y)),Y),Z) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(X,f(Y,f(f(X,Z),Y))) )).
