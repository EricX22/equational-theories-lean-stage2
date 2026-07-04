% order5v2_0486  eq1=39607 eq2=3536  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),f(Z,Z)),W),U) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(Z,Z),X)) )).
