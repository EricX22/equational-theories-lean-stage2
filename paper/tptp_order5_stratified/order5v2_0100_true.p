% order5v2_0100  eq1=26218 eq2=32171  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,Z),Z)),f(W,Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,f(f(X,f(Z,X)),W)),X) )).
