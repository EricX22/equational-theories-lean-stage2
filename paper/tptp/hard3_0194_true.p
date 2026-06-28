% hard3_0194  eq1=1709 eq2=1941  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,X),f(f(Z,Z),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(Y,Z)),f(X,X)) )).
