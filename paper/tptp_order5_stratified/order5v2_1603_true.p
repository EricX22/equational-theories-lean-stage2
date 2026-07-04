% order5v2_1603  eq1=37005 eq2=20356  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),f(X,X)),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(W,f(X,W)),Y)) )).
