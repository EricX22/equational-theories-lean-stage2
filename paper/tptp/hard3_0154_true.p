% hard3_0154  eq1=1281 eq2=3397  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(X,X),Z),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(Z,f(Y,f(X,Y))) )).
