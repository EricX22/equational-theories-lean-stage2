% hard3_0081  eq1=623 eq2=1035  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(X,f(X,f(f(Y,Y),Y))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(f(Y,f(X,X)),X)) )).
