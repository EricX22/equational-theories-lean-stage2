% hard3_0157  eq1=1328 eq2=1078  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,Y),Z),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(X,f(X,Z)),X)) )).
