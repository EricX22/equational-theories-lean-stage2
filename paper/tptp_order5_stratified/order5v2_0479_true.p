% order5v2_0479  eq1=38331 eq2=59507  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,f(f(X,Z),Y)),W),U) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,Y),Y) = f(Z,f(f(X,Z),Z)) )).
