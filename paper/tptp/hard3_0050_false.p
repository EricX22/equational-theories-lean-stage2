% hard3_0050  eq1=315 eq2=4196  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( f(X,X) = f(Y,f(Y,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(f(Z,X),Y),Y) )).
