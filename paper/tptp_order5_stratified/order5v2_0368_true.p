% order5v2_0368  eq1=30017 eq2=6908  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,f(Z,f(W,f(Y,X)))),U) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(Y,f(f(Z,Y),f(W,Z)))) )).
