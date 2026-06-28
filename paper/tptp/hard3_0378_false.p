% hard3_0378  eq1=3811 eq2=3852  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(f(Z,Y),f(Z,Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(Z,W),f(W,Y)) )).
