% hard3_0349  eq1=3283 eq2=4316  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,X) = f(Y,f(Y,f(Y,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,f(Y,X)) = f(X,f(Z,X)) )).
