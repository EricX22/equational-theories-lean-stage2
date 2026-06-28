% hard3_0076  eq1=549 eq2=1966  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(X,f(W,X)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(Z,X)),f(Z,X)) )).
