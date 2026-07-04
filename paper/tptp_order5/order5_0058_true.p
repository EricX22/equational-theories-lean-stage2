% order5_0058  eq1=27119 eq2=45051  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,W)),f(U,X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,X) = f(X,f(f(f(X,Y),Z),W)) )).
