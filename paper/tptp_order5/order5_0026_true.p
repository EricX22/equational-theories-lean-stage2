% order5_0026  eq1=46488 eq2=16234  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,X),f(W,f(W,W))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(f(f(f(Y,Z),X),W),X)) )).
