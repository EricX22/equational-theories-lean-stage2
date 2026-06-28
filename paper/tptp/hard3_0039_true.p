% hard3_0039  eq1=209 eq2=1430  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(X,f(Y,X)),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,X),f(X,f(Y,Z))) )).
