% order5v2_1140  eq1=19242 eq2=58206  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),f(f(X,X),f(Z,Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,X),X) = f(X,f(Y,f(Z,W))) )).
