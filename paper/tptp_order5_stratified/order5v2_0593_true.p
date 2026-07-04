% order5v2_0593  eq1=26832 eq2=57288  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,X),f(X,X)),f(Z,W)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(W,f(U,Y)),U) )).
