% hard3_0370  eq1=3683 eq2=3593  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,X) = f(f(Y,X),f(Z,W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(Z,f(f(X,Z),W)) )).
