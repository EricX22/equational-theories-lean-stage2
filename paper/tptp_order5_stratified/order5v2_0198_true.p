% order5v2_0198  eq1=18984 eq2=27067  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,X),f(f(Y,Y),f(Z,Y))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,Y)),f(X,Z)) )).
