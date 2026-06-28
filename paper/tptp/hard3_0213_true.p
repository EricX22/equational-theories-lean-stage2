% hard3_0213  eq1=2004 eq2=3883  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,Z)),f(W,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(Y,f(X,Z)),X) )).
