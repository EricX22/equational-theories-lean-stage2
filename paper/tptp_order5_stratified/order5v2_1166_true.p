% order5v2_1166  eq1=44646 eq2=57305  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(Y,f(f(Z,f(W,Y)),Z)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(W,f(U,U)),W) )).
