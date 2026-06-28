% hard3_0256  eq1=2410 eq2=2456  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,f(Z,W))),X) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,f(f(Y,X),X)),X) )).
