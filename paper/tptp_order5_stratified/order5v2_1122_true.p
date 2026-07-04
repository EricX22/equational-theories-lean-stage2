% order5v2_1122  eq1=12178 eq2=37159  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,Z),Z),f(Y,Y))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(f(X,f(X,f(Y,X))),X),X) )).
