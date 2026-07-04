% order5v2_1998  eq1=15802 eq2=45597  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,f(Y,X)),X),Y)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(f(X,W),X),U)) )).
