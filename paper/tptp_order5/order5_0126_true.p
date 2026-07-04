% order5_0126  eq1=45759 eq2=21507  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(f(Z,W),Z),Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(Y,Z)),f(Y,f(Y,Z))) )).
