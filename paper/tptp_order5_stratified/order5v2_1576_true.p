% order5v2_1576  eq1=19861 eq2=4853  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,X),f(f(Y,f(Y,Z)),Y)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(Y,f(Z,f(Y,f(W,W))))) )).
