% order5_0103  eq1=27108 eq2=17544  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,W)),f(Y,U)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(X,f(W,f(W,X)))) )).
