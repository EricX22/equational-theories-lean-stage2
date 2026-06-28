% hard3_0064  eq1=424 eq2=2466  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(X,f(Y,f(Z,Z)))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,f(f(Y,Y),X)),X) )).
