% order5v2_0456  eq1=17551 eq2=17887  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,Z),f(X,f(W,f(U,Z)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,X),f(Y,f(f(Z,X),Z))) )).
