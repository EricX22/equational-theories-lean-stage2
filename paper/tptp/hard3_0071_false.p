% hard3_0071  eq1=511 eq2=2132  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(Y,f(Y,f(Y,f(X,Y)))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,Y),X),f(Z,Z)) )).
