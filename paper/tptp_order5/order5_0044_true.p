% order5_0044  eq1=59696 eq2=41731  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(f(X,Y),Z) = f(Y,f(f(Z,Z),W)) )).
fof(goal, conjecture, ! [U,V,W,X,Y,Z] : ( f(X,X) = f(Y,f(Z,f(W,f(U,V)))) )).
