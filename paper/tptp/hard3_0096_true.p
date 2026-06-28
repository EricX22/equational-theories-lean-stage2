% hard3_0096  eq1=752 eq2=203  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(X,W),X))) )).
fof(goal, conjecture, ! [X] : ( X = f(f(X,f(X,X)),X) )).
