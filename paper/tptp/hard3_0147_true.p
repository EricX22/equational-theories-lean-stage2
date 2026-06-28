% hard3_0147  eq1=1212 eq2=1041  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,f(W,W)),X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(Y,f(X,Z)),X)) )).
