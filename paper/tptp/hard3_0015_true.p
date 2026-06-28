% hard3_0015  eq1=60 eq2=3332  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(Y,f(Z,Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(X,f(Z,f(Y,W))) )).
