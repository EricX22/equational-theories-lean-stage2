% order5v2_1298  eq1=53464 eq2=55248  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(f(Z,X),Y),W),X) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,Z)) != f(X,f(f(W,Y),W)) )).
