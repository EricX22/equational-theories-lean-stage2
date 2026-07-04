% order5v2_0887  eq1=52514 eq2=3970  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( f(X,Y) = f(f(f(Y,f(Z,Y)),W),U) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(Y,f(Y,Z)),W) )).
