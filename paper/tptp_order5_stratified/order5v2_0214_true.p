% order5v2_0214  eq1=699 eq2=33774  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(X,f(f(Z,W),Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(Z,f(X,W))),X) )).
