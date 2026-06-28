% hard3_0245  eq1=2232 eq2=3261  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(U,X)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(X,f(Y,f(Y,X))) )).
