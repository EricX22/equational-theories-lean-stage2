% order5_0234  eq1=41357 eq2=56665  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(f(Y,Z),Z),Z),W),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,X)) = f(f(X,f(Z,Y)),X) )).
