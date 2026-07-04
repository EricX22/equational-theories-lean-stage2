% order5_0062  eq1=59990 eq2=38497  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(f(X,X),X) = f(f(Y,Z),f(Z,Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,f(f(Y,Z),Z)),W),Z) )).
