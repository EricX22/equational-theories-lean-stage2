% hard3_0225  eq1=2083 eq2=2243  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,Y),Z),f(W,Y)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,f(X,f(Y,X))),X) )).
