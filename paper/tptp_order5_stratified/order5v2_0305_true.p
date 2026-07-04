% order5v2_0305  eq1=39665 eq2=49619  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),f(W,Y)),Y),X) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,X) = f(f(Y,f(Z,f(W,U))),X) )).
