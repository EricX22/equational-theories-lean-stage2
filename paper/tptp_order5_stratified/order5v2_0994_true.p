% order5v2_0994  eq1=2138 eq2=24732  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(Y,Y),Y),f(Y,Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(f(X,Y),Z)) )).
