% hard3_0352  eq1=3328 eq2=3313  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(X,f(Z,f(X,W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(X,f(Z,Z))) )).
