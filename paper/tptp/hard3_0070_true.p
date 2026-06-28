% hard3_0070  eq1=487 eq2=114  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(X,f(Z,f(Y,X)))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(Y,f(f(X,X),X)) )).
