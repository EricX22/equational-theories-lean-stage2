% hard3_0346  eq1=3277 eq2=4365  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(X,f(Z,W))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,f(Y,Z)) != f(Y,f(Z,W)) )).
