% hard3_0260  eq1=2478 eq2=2287  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(f(Y,Z),X)),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,f(Y,f(Z,W))),Z) )).
