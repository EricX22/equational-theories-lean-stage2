% hard3_0282  eq1=2678 eq2=1861  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(Y,Z)),W) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(X,f(Y,Y)),f(Y,Y)) )).
