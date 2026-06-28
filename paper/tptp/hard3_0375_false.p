% hard3_0375  eq1=3773 eq2=4134  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(f(Y,Z),f(Y,Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(X,Y) != f(f(f(X,Y),Z),Y) )).
