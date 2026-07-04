% order5v2_0634  eq1=37127 eq2=20357  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),f(U,W)),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(W,f(X,W)),Z)) )).
