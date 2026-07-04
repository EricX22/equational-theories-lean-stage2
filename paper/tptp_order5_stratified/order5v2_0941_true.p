% order5v2_0941  eq1=9359 eq2=5301  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(X,Z),f(X,f(X,Z)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(Y,f(Y,f(Y,W))))) )).
