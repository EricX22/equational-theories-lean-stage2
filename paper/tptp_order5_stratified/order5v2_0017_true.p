% order5v2_0017  eq1=43976 eq2=57939  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(Z,f(f(Z,Z),f(X,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(f(Y,Z),Z),X) )).
