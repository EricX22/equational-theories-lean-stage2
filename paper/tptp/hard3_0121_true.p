% hard3_0121  eq1=994 eq2=2628  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(X,X))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,W),Z)),X) )).
