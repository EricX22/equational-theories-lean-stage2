% hard3_0131  eq1=1047 eq2=1463  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Y,X)),Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,Y),f(Z,f(X,Z))) )).
