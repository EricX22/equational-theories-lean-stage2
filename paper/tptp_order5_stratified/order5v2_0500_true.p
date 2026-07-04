% order5v2_0500  eq1=10407 eq2=36142  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Y,Z),f(f(Y,Y),Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,W)),f(X,W)),Y) )).
