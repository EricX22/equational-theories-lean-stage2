% hard3_0372  eq1=3728 eq2=4508  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(f(X,Y),f(Z,Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(Y,Z)) != f(f(X,X),Z) )).
