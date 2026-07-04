% order5v2_0340  eq1=22105 eq2=60116  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,W)),f(X,f(Z,Y))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,X),Y) = f(f(Z,Z),f(Z,Z)) )).
