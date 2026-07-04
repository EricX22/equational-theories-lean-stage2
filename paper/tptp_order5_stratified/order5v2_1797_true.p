% order5v2_1797  eq1=40942 eq2=47234  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(f(Y,X),Z),X),W),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(Y,Z),f(f(X,W),W)) )).
