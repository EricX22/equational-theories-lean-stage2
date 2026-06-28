% hard3_0152  eq1=1252 eq2=1020  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(X,f(f(f(Y,Y),Y),Y)) )).
fof(goal, conjecture, ! [X] : ( X = f(X,f(f(X,f(X,X)),X)) )).
