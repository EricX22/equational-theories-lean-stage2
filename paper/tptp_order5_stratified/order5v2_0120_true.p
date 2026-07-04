% order5v2_0120  eq1=16597 eq2=49176  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(f(Y,Z),W),U),Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Z,Y),Z),f(W,W)) )).
