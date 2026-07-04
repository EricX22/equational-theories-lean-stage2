% order5v2_0505  eq1=18348 eq2=23019  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,Y),f(Z,f(f(W,W),U))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(Y,f(Z,W)),f(f(Y,U),Z)) )).
