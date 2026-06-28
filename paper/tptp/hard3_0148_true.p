% hard3_0148  eq1=1217 eq2=2056  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(W,U)),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,Y),X),f(Z,X)) )).
