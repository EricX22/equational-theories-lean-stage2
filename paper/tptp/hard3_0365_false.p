% hard3_0365  eq1=3536 eq2=326  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(Z,Z),X)) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,Y) != f(X,f(Y,Y)) )).
