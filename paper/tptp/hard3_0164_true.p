% hard3_0164  eq1=1484 eq2=2351  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,X),f(X,f(Z,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(Y,f(Z,Y))),X) )).
