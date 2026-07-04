% order5v2_1241  eq1=39242 eq2=16482  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,X),f(Z,W)),W),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(f(f(Y,X),Z),W),X)) )).
