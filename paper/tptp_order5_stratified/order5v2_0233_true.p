% order5v2_0233  eq1=27148 eq2=29527  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(X,Y)),f(Y,Z)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(Y,f(X,f(Y,f(Z,W)))),U) )).
