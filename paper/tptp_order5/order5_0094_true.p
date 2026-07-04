% order5_0094  eq1=23375 eq2=59370  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,X),Y),f(Z,f(X,W))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,Y),X) = f(Z,f(f(Y,Y),W)) )).
