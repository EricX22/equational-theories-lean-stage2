% hard3_0395  eq1=4545 eq2=4279  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(Z,Y),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,f(X,X)) != f(Y,f(Z,Y)) )).
