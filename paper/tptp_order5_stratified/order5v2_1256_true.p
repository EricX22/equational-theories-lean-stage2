% order5v2_1256  eq1=20230 eq2=5544  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),f(f(Y,f(Z,Z)),Z)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(W,f(U,f(Y,W))))) )).
