% order5_0182  eq1=14724 eq2=4807  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,X),f(Z,Z)),X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(Y,f(Y,f(Z,f(X,W))))) )).
