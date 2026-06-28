% hard3_0050  eq1=315 eq2=4196  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( f(X,X) = f(Y,f(Y,X)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(f(Z,X),Y),Y) )).
