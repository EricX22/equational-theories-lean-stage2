% order5v2_0758  eq1=34786 eq2=20843  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,X),f(f(Y,Z),W)),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,Y),f(f(f(X,X),Z),Z)) )).
