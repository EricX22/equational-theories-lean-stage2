% order5v2_1470  eq1=38088 eq2=54747  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,f(f(Y,X),Y)),Y),Z) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,f(X,Y)) != f(X,f(f(Y,X),Y)) )).
