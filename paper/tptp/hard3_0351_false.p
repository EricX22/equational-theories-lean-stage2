% hard3_0351  eq1=3321 eq2=3535  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(X,f(Y,f(Z,X))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(X,f(f(Z,Y),W)) )).
