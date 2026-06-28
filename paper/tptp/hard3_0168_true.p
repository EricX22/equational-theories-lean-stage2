% hard3_0168  eq1=1506 eq2=359  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,X),f(Z,f(Z,X))) )).
fof(goal, conjecture, ! [X] : ( f(X,X) = f(f(X,X),X) )).
