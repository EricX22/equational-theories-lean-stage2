% order5v2_0461  eq1=11052 eq2=1023  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(X,f(X,Y)),f(Y,Z))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(f(X,f(X,Y)),Y)) )).
