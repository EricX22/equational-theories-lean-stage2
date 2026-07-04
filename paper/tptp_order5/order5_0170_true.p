% order5_0170  eq1=50371 eq2=56031  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(f(Y,f(f(X,Z),X)),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,Y)) = f(f(Z,Z),f(Z,X)) )).
