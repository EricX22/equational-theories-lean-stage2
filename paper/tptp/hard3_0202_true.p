% hard3_0202  eq1=1874 eq2=3524  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(X,f(Y,Z)),f(Y,W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(Y,Z),X)) )).
