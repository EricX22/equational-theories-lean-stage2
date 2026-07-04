% order5_0150  eq1=35154 eq2=52659  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),f(f(Y,W),Y)),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Z,f(Y,Y)),Y),W) )).
