% order5v2_0928  eq1=45787 eq2=309  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(f(W,X),Z),U)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(X,f(Y,X)) )).
