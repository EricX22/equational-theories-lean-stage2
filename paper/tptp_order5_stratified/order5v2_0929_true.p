% order5v2_0929  eq1=15925 eq2=4067  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,f(Z,Z)),W),Y)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(f(f(X,X),Y),X) )).
