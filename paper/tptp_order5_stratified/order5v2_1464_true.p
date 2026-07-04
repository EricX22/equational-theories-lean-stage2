% order5v2_1464  eq1=11682 eq2=5172  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,f(W,U)),f(Y,Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(Y,f(Z,f(Z,f(W,W))))) )).
