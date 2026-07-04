% order5v2_1004  eq1=9779 eq2=34483  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Z,Z),f(Z,f(Y,Z)))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,f(U,Y))),Y) )).
