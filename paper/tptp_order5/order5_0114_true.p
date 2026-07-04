% order5_0114  eq1=17498 eq2=43574  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(X,f(Y,f(X,W)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(X,f(f(Z,X),f(W,Z))) )).
