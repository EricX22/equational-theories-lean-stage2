% order5v2_1884  eq1=36733 eq2=49669  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(f(Y,Y),Z),f(Z,Y)),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(X,f(Y,f(X,Z))),Y) )).
