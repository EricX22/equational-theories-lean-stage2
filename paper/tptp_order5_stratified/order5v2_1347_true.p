% order5v2_1347  eq1=47000 eq2=61711  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(X,X),f(f(X,Z),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,X),X) = f(f(f(X,Y),Z),X) )).
