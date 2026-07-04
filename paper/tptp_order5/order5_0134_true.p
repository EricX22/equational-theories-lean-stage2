% order5_0134  eq1=7063 eq2=61670  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(Y,Y),f(W,W)))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(f(X,Y),Z) = f(f(W,f(U,Y)),Y) )).
