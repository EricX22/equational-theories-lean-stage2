% order5v2_0490  eq1=13167 eq2=60927  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(X,f(W,U))),W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,X),Y) = f(f(Y,f(Y,Y)),Z) )).
