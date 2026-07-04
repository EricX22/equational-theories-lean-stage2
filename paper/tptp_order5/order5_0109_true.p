% order5_0109  eq1=56488 eq2=45673  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,f(X,X)) = f(f(Y,f(Z,W)),W) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(f(Y,W),X),W)) )).
