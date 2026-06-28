% hard3_0176  eq1=1571 eq2=2541  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),f(Y,f(X,Z))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(Y,f(f(Y,Y),X)),Y) )).
