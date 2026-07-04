% order5v2_1759  eq1=16481 eq2=49860  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(f(f(Y,X),Z),Z),W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Y,f(Z,f(X,Z))),Z) )).
