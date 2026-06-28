% hard3_0022  eq1=103 eq2=3519  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(f(X,Y),Z)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(X,f(f(Y,X),Y)) )).
