% order5v2_1599  eq1=29476 eq2=48301  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(X,f(X,f(Z,X)))),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(Y,W)),f(X,X)) )).
