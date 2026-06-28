% hard3_0068  eq1=456 eq2=1051  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(Y,f(Z,f(Z,Z)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Y,Z)),X)) )).
