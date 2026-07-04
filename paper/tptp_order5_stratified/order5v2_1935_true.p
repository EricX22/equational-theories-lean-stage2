% order5v2_1935  eq1=40426 eq2=37013  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,f(Z,Y)),W),W),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),f(X,Z)),X) )).
