% order5_0147  eq1=4995 eq2=54404  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(X,f(Z,f(Y,f(Y,Z))))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(Y,f(X,f(W,W))) )).
