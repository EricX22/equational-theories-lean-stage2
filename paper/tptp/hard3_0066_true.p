% hard3_0066  eq1=435 eq2=1678  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(X,f(Y,f(X,f(Z,W)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,Y),f(f(Z,W),Z)) )).
