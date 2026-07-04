% order5_0105  eq1=12401 eq2=14382  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,Z),Y),f(W,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(f(X,Y),f(Z,Y)),Y)) )).
