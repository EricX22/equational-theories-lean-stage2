% hard3_0263  eq1=2493 eq2=3052  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(Y,f(f(X,X),X)),X) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(f(X,X),X),Y),X) )).
