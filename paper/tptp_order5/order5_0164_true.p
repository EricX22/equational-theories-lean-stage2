% order5_0164  eq1=38121 eq2=8003  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(X,f(f(Y,Y),Y)),X),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(Z,f(f(Z,f(Y,X)),Y))) )).
