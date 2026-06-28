% hard3_0251  eq1=2268 eq2=1851  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(Y,f(Y,Y))),Z) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,f(Y,X)),f(Y,Y)) )).
