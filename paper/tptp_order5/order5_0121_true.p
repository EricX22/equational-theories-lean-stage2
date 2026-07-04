% order5_0121  eq1=10989 eq2=34489  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(X,f(f(Y,f(Z,Y)),f(W,X))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,f(U,Z))),Y) )).
