% order5v2_1317  eq1=33033 eq2=15865  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(f(X,Y),Z),W)),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,f(Y,W)),Z),W)) )).
