% hard3_0160  eq1=1433 eq2=4631  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,X),f(Y,f(X,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,Y),X) = f(f(X,Z),X) )).
