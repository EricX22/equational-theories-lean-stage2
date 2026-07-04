% order5v2_1272  eq1=5105 eq2=7673  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Y,f(Y,f(Y,f(Z,W))))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(Y,f(X,f(f(Z,f(W,W)),U))) )).
