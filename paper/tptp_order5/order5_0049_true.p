% order5_0049  eq1=6217 eq2=23275  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(Y,f(f(W,Z),Z)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(X,Y),Z),f(Z,f(X,W))) )).
