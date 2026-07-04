% order5v2_1640  eq1=28183 eq2=50106  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,f(Z,Z)),Y),f(Z,Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Z,f(Z,f(Y,Z))),X) )).
