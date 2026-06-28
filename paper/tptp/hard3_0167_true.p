% hard3_0167  eq1=1487 eq2=3389  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,X),f(X,f(Z,W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(Z,f(X,f(Z,Z))) )).
