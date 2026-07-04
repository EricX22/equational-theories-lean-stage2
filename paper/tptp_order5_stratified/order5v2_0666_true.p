% order5v2_0666  eq1=40372 eq2=16706  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,f(Z,Y)),X),W),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(f(f(Z,Y),Y),Z),W)) )).
