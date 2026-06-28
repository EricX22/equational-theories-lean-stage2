% hard3_0325  eq1=3034 eq2=3762  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,W)),Z),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(f(Y,Y),f(Y,Y)) )).
