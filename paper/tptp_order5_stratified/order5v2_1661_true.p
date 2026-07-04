% order5v2_1661  eq1=9643 eq2=37962  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,X),f(W,f(Y,Z)))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(f(Y,f(Z,f(W,W))),X),U) )).
