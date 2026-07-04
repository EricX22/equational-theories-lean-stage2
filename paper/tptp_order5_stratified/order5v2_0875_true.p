% order5v2_0875  eq1=30436 eq2=16918  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(X,f(f(Z,Y),W))),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(f(f(Z,W),W),Y),W)) )).
