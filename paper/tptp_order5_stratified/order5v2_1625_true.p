% order5v2_1625  eq1=13038 eq2=19908  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Y,f(Z,f(Y,Y))),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,X),f(f(Z,f(Y,Z)),Z)) )).
