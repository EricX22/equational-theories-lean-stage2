% order5_0097  eq1=44026 eq2=46458  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(f(W,X),f(Y,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Z,X),f(Z,f(Y,Y))) )).
