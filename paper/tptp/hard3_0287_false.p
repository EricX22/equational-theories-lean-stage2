% hard3_0287  eq1=2683 eq2=3715  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(X,Y),f(Z,Y)),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(X,X),f(Y,Y)) )).
