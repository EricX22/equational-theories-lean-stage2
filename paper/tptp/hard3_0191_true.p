% hard3_0191  eq1=1687 eq2=3312  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,X),f(f(X,Z),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(X,f(Z,Y))) )).
