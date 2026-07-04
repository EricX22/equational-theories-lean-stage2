% order5v2_0200  eq1=50282 eq2=4639  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(W,f(U,W))),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,Y),X) = f(f(Y,Z),Y) )).
